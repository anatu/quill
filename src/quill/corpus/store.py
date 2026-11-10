"""corpus.sqlite: posts, chunks, dropped blocks, AI-text flags.

`ingest` rebuilds posts, chunks, dropped_blocks and meta. It never touches ai_flags,
so review decisions survive a rebuild.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
  file TEXT PRIMARY KEY, slug TEXT, url TEXT, date TEXT, year INTEGER, title TEXT, byline TEXT,
  fetched TEXT, consent_ref TEXT, words INTEGER, quote_words INTEGER, kept INTEGER, drop_reason TEXT,
  twin_group TEXT, twin_links TEXT, tags TEXT, hrefs TEXT, text TEXT);
CREATE TABLE IF NOT EXISTS chunks (
  id TEXT PRIMARY KEY, post_file TEXT REFERENCES posts(file), seq INTEGER, twin_group TEXT,
  words INTEGER, length_bucket TEXT, text TEXT, flags TEXT, text_marked TEXT);
CREATE TABLE IF NOT EXISTS dropped_blocks (post_file TEXT, reason TEXT, words INTEGER, text TEXT);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS ai_flags (
  post_file TEXT PRIMARY KEY, flags TEXT, detail TEXT, decision TEXT DEFAULT 'pending', note TEXT,
  decided TEXT);
CREATE INDEX IF NOT EXISTS chunks_post ON chunks(post_file);
DROP VIEW IF EXISTS usable_chunks;
CREATE VIEW usable_chunks AS
  SELECT c.* FROM chunks c JOIN posts p ON p.file = c.post_file
  WHERE p.kept = 1 AND c.post_file NOT IN (SELECT post_file FROM ai_flags WHERE decision = 'drop');
"""
REBUILT = ("chunks", "dropped_blocks", "posts", "meta")


def connect(path: Path) -> sqlite3.Connection:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db


def db_path(cfg: dict) -> Path:
    return Path(cfg["paths"]["corpus"]) / "corpus.sqlite"


def write_corpus(db: sqlite3.Connection, posts: list[dict], meta: dict) -> None:
    for t in REBUILT:                  # drop, not delete: the schema may have changed
        db.execute(f"DROP TABLE IF EXISTS {t}")
    db.executescript(SCHEMA)
    with db:
        for p in posts:
            db.execute(
                "INSERT INTO posts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["file"], p["slug"], p["url"], p["date"], int(p["date"][:4]) if p["date"] else None, p["title"],
                 p["author"], p["fetched"], p["consent_ref"], p["words"], p["quote_words"], int(p["kept"]),
                 p.get("drop_reason"), p.get("twin_group"), json.dumps(p.get("twin_links", [])),
                 json.dumps(p.get("tags", [])), json.dumps(p.get("hrefs", [])), "\n\n".join(b["text"] for b in p["blocks"])))
            db.executemany("INSERT INTO dropped_blocks VALUES (?,?,?,?)",
                           [(p["file"], d["reason"], d["words"], d["text"]) for d in p["dropped"]])
            db.executemany("INSERT INTO chunks VALUES (?,?,?,?,?,?,?,?,?)",
                           [(c["id"], p["file"], i, p.get("twin_group"), c["words"], c["bucket"], c["text"],
                             json.dumps(c["flags"]), c.get("text_marked")) for i, c in enumerate(p.get("chunks", []))])
        db.executemany("INSERT INTO meta VALUES (?,?)", [(k, json.dumps(v)) for k, v in meta.items()])


def set_meta(db: sqlite3.Connection, key: str, value) -> None:
    with db:
        db.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (key, json.dumps(value)))


def get_meta(db: sqlite3.Connection, key: str, default=None):
    r = db.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return json.loads(r["value"]) if r else default


def kept_posts(db: sqlite3.Connection) -> list[sqlite3.Row]:
    return db.execute("SELECT * FROM posts WHERE kept = 1 ORDER BY date, file").fetchall()
