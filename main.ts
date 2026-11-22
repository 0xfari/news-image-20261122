// news-image-20261122 — entrypoint.
//
// The front page is pre-rendered as entry.png (1024x1024, RGB, 111,845 bytes).
// This program validates that the file is a whole, well-formed PNG and then
// publishes exactly those bytes to the grader output directory.
//
// Runs on Node 22 with type stripping, standard library only, no network.
import { createHash } from 'node:crypto';
import { mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;
const IMAGE_WIDTH = 1024;
const IMAGE_HEIGHT = 1024;

function fail(message: string): never {
  throw new Error(`news-image-20261122: ${message}`);
}

// The image lives next to this file; the repository is mounted read-only at
// grading time, so resolve it from the module URL, never from the cwd.
function imagePath(): string {
  return fileURLToPath(new URL('./entry.png', import.meta.url));
}

function checkPng(png: Buffer): void {
  if (png.length > MAX_BYTES) {
    fail(`entry.png is ${png.length} bytes, over the 1 MiB cap`);
  }
  if (png.length < 8 || !png.subarray(0, 8).equals(PNG_MAGIC)) {
    fail('entry.png does not start with the PNG signature');
  }
  if (png.length < 29) {
    fail('entry.png is too short to hold an IHDR chunk');
  }
  // First chunk must be IHDR: length 13, type "IHDR", 13 bytes of data.
  const ihdrLength = png.readUInt32BE(8);
  const ihdrType = png.subarray(12, 16).toString('latin1');
  if (ihdrLength !== 13 || ihdrType !== 'IHDR') {
    fail('entry.png does not start with an IHDR chunk');
  }
  const width = png.readUInt32BE(16);
  const height = png.readUInt32BE(20);
  if (width !== IMAGE_WIDTH || height !== IMAGE_HEIGHT) {
    fail(`entry.png is ${width}x${height}, expected ${IMAGE_WIDTH}x${IMAGE_HEIGHT}`);
  }
  // Last chunk must be IEND: zero-length chunk, type "IEND", standard CRC.
  const tail = png.subarray(png.length - 12);
  const iendLength = tail.readUInt32BE(0);
  const iendType = tail.subarray(4, 8).toString('latin1');
  const iendCrc = tail.readUInt32BE(8);
  if (iendLength !== 0 || iendType !== 'IEND' || iendCrc !== 0xae426082) {
    fail('entry.png does not end with a valid IEND chunk');
  }
  checkChunks(png);
}

// CRC-32 (IEEE, polynomial 0xedb88320) over a chunk's type + data must equal
// the CRC stored after the data. Verifies every chunk, not just the ends.
const CRC_TABLE: number[] = (() => {
  const table: number[] = [];
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table.push(c >>> 0);
  }
  return table;
})();

function crc32(buf: Buffer): number {
  let crc = 0xffffffff;
  for (const byte of buf) crc = CRC_TABLE[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}

function checkChunks(png: Buffer): void {
  let offset = 8;
  let seenIdat = false;
  while (offset < png.length) {
    if (offset + 12 > png.length) fail('entry.png has a truncated chunk header');
    const length = png.readUInt32BE(offset);
    const type = png.subarray(offset + 4, offset + 8).toString('latin1');
    const end = offset + 12 + length;
    if (end > png.length) fail(`entry.png chunk ${type} overruns the file`);
    const stored = png.readUInt32BE(offset + 8 + length);
    const actual = crc32(png.subarray(offset + 4, offset + 8 + length));
    if (stored !== actual) fail(`entry.png chunk ${type} fails its CRC check`);
    if (type === 'IDAT') seenIdat = true;
    if (type === 'IEND') {
      if (end !== png.length) fail('entry.png has bytes after the IEND chunk');
      break;
    }
    offset = end;
  }
  if (!seenIdat) fail('entry.png holds no IDAT chunk');
  // IHDR data: width, height, bit depth 8, colour type 2 (truecolour RGB),
  // compression 0, filter 0, interlace 0 (none) or 1 (Adam7).
  const bitDepth = png[24];
  const colourType = png[25];
  const compression = png[26];
  const filter = png[27];
  const interlace = png[28];
  if (bitDepth !== 8 || colourType !== 2 || compression !== 0 || filter !== 0 || (interlace !== 0 && interlace !== 1)) {
    fail(`entry.png IHDR fields unexpected (depth ${bitDepth}, colour ${colourType}, compression ${compression}, filter ${filter}, interlace ${interlace})`);
  }
}

// Empty the output directory's CONTENTS only. The grader mounts /output, so
// removing the directory itself fails with EBUSY (Pelajaran 37).
function clearOutputDir(outDir: string): void {
  mkdirSync(outDir, { recursive: true });
  for (const name of readdirSync(outDir)) {
    rmSync(join(outDir, name), { recursive: true, force: true });
  }
}

function main(): void {
  const png = readFileSync(imagePath());
  checkPng(png);

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  clearOutputDir(outDir);
  const outPath = join(outDir, 'entry.png');
  writeFileSync(outPath, png);

  // Post-write byte comparison: what the grader reads must be exactly the
  // bytes we validated.
  const written = readFileSync(outPath);
  if (!written.equals(png)) {
    fail('output differs from entry.png after write');
  }
  const digest = createHash('sha256').update(written).digest('hex');
  console.log(`wrote ${outPath} (${written.length} bytes, sha256 ${digest})`);
}

main();
