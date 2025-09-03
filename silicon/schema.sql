-- We do not open sqlite3 in WAL mode, because:
-- 1. Raw database performance is not exactly a critical goal here.
-- 2. WAL mode creates two small files every time the database is open. This is
--    not a big burden, but it seems worth avoiding if there's no actual
--    benefit.

CREATE TABLE pages (
    revision TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    PRIMARY KEY (revision, title)
);

-- Page relationships
CREATE TABLE relationships (
    title_a TEXT NOT NULL,
    title_b TEXT NOT NULL
);

-- The full-text search table
CREATE virtual TABLE pages_fts USING FTS5(
    title,
    body
);

-- Before a page is inserted into the pages table,
-- delete the old matching entry in the FTS table.
-- Then, insert the new page into the FTS table.
CREATE TRIGGER pages_after_insert AFTER INSERT ON pages
BEGIN
    DELETE FROM pages_fts WHERE title = new.title;
    INSERT INTO pages_fts (title, body)
    VALUES (new.title, new.body);
END;

-- Same trigger, but for an UPDATE (used in the `page.write()` upsert)
CREATE TRIGGER pages_after_update AFTER UPDATE ON pages
BEGIN
    DELETE FROM pages_fts WHERE title = new.title;
    INSERT INTO pages_fts (title, body)
    VALUES (new.title, new.body);
END;
