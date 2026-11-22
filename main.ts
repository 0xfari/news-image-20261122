// main.ts — validate entry.png and copy it to MAKEFUN_OUTPUT_DIR.
//
// Node 22, standard library only. No network. The output directory is never
// removed itself (on the grader it is a mount point; deleting it fails with
// EBUSY) — only its contents are cleared before the copy lands.
// The program is deterministic: the same input bytes produce the same output
// bytes on every run, and the copy is verified byte for byte.
import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, rmSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = join(HERE, "entry.png");
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const MAX_BYTES = 1048576;
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const CRC_TABLE: number[] = (() => {
  const table: number[] = [];
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(buf: Buffer): number {
  let c = 0xffffffff;
  for (const b of buf) c = CRC_TABLE[(c ^ b) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

function main(): void {
  if (!existsSync(SRC)) fail(`entry.png not found next to main.ts (${SRC})`);
  const bytes = readFileSync(SRC);
  if (bytes.length > MAX_BYTES) {
    fail(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
  }
  if (bytes.length < 8 || !bytes.subarray(0, 8).equals(PNG_SIG)) {
    fail("entry.png does not start with the PNG signature");
  }
  // IHDR must be the first chunk: length 13, type IHDR, then width/height.
  if (bytes.length < 33) fail("entry.png is too short for an IHDR chunk");
  const ihdrLen = bytes.readUInt32BE(8);
  const ihdrType = bytes.subarray(12, 16).toString("latin1");
  if (ihdrLen !== 13 || ihdrType !== "IHDR") {
    fail(`first chunk is not a 13-byte IHDR (len ${ihdrLen}, type ${ihdrType})`);
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  const bitDepth = bytes[24];
  const colorType = bytes[25];
  if (width !== 1024 || height !== 1024) {
    fail(`entry.png is ${width}x${height}, expected 1024x1024`);
  }
  if (bitDepth !== 8 || colorType !== 2) {
    fail(`unexpected IHDR: bit depth ${bitDepth}, color type ${colorType}`);
  }
  const ihdrCrcStored = bytes.readUInt32BE(29);
  const ihdrCrc = crc32(bytes.subarray(12, 29));
  if (ihdrCrc !== ihdrCrcStored) fail("IHDR chunk CRC mismatch");
  // The file must end with a well-formed IEND chunk (12 bytes).
  const tail = bytes.subarray(bytes.length - 12);
  if (tail.readUInt32BE(0) !== 0 || tail.subarray(4, 8).toString("latin1") !== "IEND") {
    fail("entry.png does not end with an IEND chunk");
  }
  const iendCrc = crc32(bytes.subarray(bytes.length - 8, bytes.length - 4));
  if (iendCrc !== tail.readUInt32BE(8)) fail("IEND chunk CRC mismatch");

  mkdirSync(OUT_DIR, { recursive: true });
  for (const name of readdirSync(OUT_DIR)) {
    rmSync(join(OUT_DIR, name), { recursive: true, force: true });
  }
  const dest = join(OUT_DIR, "entry.png");
  copyFileSync(SRC, dest);
  const copied = readFileSync(dest);
  if (!copied.equals(bytes)) fail("copied entry.png differs from the source");
  const sha = createHash("sha256").update(bytes).digest("hex");
  const size = statSync(dest).size;
  console.log(`entry.png ${width}x${height} ${size} bytes sha256 ${sha} -> ${dest}`);
}

main();
