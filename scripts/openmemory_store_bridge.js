#!/usr/bin/env node

const fs = require("fs");

const root = process.env.OPENMEMORY_JS_ROOT;
if (!root) {
  process.stderr.write("OPENMEMORY_JS_ROOT is required\n");
  process.exit(1);
}

const { Memory } = require(`${root}/dist/core/memory.js`);
const { q } = require(`${root}/dist/core/db.js`);
const { delete_memory, update_memory } = require(`${root}/dist/memory/hsg.js`);

function parseJson(value, fallback) {
  try {
    return typeof value === "string" ? JSON.parse(value) : (value ?? fallback);
  } catch {
    return fallback;
  }
}

function hasProjectKeyTag(tags, projectKeyTag) {
  return Array.isArray(tags) && tags.includes(projectKeyTag);
}

function getContentHash(meta) {
  return meta && typeof meta === "object" ? meta.content_hash : undefined;
}

async function upsertProjectMemory(payload) {
  const userId = payload.user_id || undefined;
  const tags = Array.isArray(payload.tags) ? payload.tags : [];
  const metadata = payload.metadata || {};
  const memory = new Memory(userId || null);
  const projectKeyTag = tags.find((tag) => typeof tag === "string" && tag.startsWith("project-key:"));
  if (!userId || !projectKeyTag) {
    return await memory.add(payload.content, { user_id: userId, tags, ...metadata });
  }

  const rows = await q.all_mem_by_user.all(userId, 1000, 0);
  const projectRows = rows.filter((row) => {
    const rowTags = parseJson(row.tags, []);
    return hasProjectKeyTag(rowTags, projectKeyTag);
  });
  const targetHash = getContentHash(metadata);
  const exact = projectRows.find((row) => getContentHash(parseJson(row.meta, {})) === targetHash);
  const keeper = exact || projectRows[0] || null;

  let result;
  if (keeper) {
    result = await update_memory(keeper.id, payload.content, tags, metadata);
    result = { ...result, primary_sector: keeper.primary_sector, sectors: [keeper.primary_sector] };
    for (const row of projectRows) {
      if (row.id !== keeper.id) {
        await delete_memory(row.id);
      }
    }
  } else {
    result = await memory.add(payload.content, { user_id: userId, tags, ...metadata });
  }
  return result;
}

async function main() {
  const raw = fs.readFileSync(0, "utf8");
  const payload = JSON.parse(raw);
  const result = await upsertProjectMemory(payload);
  process.stdout.write(`${JSON.stringify(result)}\n`);
  process.exit(0);
}

main().catch((error) => {
  const message = error && error.stack ? error.stack : String(error);
  process.stderr.write(`${message}\n`);
  process.exit(1);
});
