// Entry point for the 22 November 2026 news-image round.
//
// The grader runs this file with Node 22 and expects exactly one file
// in the output directory: the front-page image shipped next to this
// script, copied byte for byte.
//
// Two properties of the grading sandbox shape the code below:
//  * the output directory is a mount point, so the program may delete
//    what is inside it but must never delete the directory itself;
//  * there is no network, so the image must already be on disk.

import { mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const IMAGE = "entry.png";
const OUT_DIR = process.env["MAKEFUN_OUTPUT_DIR"] ?? "/output";
const MAX_EDGE = 1024;
const MAX_BYTES = 1024 * 1024;

// First eight bytes of every PNG file.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function die(message: string): never {
  throw new Error(message);
}

function loadEntry(): { data: Buffer; width: number; height: number } {
  const path = new URL(`./${IMAGE}`, import.meta.url);
  let data: Buffer;
  try {
    data = readFileSync(path);
  } catch (err) {
    die(`cannot read ${IMAGE}: ${(err as Error).message}`);
  }
  if (data.length > MAX_BYTES) {
    die(`${IMAGE} is ${data.length} bytes, over the ${MAX_BYTES} byte cap`);
  }
  if (data.length < 24 || !data.subarray(0, 8).equals(PNG_MAGIC)) {
    die(`${IMAGE} does not start with the PNG signature`);
  }
  if (data.toString("ascii", 12, 16) !== "IHDR") {
    die(`${IMAGE} has no IHDR chunk at offset 12`);
  }
  const width = data.readUInt32BE(16);
  const height = data.readUInt32BE(20);
  if (width === 0 || height === 0) {
    die(`${IMAGE} has a zero dimension`);
  }
  if (width > MAX_EDGE || height > MAX_EDGE) {
    die(`${IMAGE} is ${width}x${height}, over the ${MAX_EDGE}x${MAX_EDGE} cap`);
  }
  // A well-formed PNG ends with a 12-byte IEND chunk (zero length,
  // tag "IEND", CRC). Refuse a file that is truncated mid-stream.
  if (
    data.length < 36 ||
    data.readUInt32BE(data.length - 12) !== 0 ||
    data.toString("ascii", data.length - 8, data.length - 4) !== "IEND"
  ) {
    die(`${IMAGE} has no IEND trailer — the file looks truncated`);
  }
  return { data, width, height };
}

function clearOutput(dir: string): void {
  mkdirSync(dir, { recursive: true });
  for (const name of readdirSync(dir)) {
    rmSync(join(dir, name), { force: true, recursive: true });
  }
}

function publish(data: Buffer): void {
  const target = join(OUT_DIR, IMAGE);
  writeFileSync(target, data);
  const back = readFileSync(target);
  if (back.length !== data.length || !back.equals(data)) {
    die(`verification failed: ${target} differs from ${IMAGE}`);
  }
}

function main(): void {
  const { data, width, height } = loadEntry();
  clearOutput(OUT_DIR);
  publish(data);
  console.log(`wrote ${IMAGE} (${width}x${height}, ${data.length} bytes) to ${OUT_DIR}`);
}

try {
  main();
} catch (err) {
  console.error(`main.ts: ${(err as Error).message}`);
  process.exit(1);
}
