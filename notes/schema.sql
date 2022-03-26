-- Because we (generally) keep all revisions, most mutable operations on this
-- will be INSERTs with a few deletes from time to time. No UPDATEs.
CREATE TABLE IF NOT EXISTS pages (
    revision TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT
);

-- creating the index should be done after the inserts on bulk import of data
CREATE INDEX IF NOT EXISTS pages_idx ON pages (
  revision,
  title
);

-- Page relationships
CREATE TABLE relationships (
    title_a TEXT NOT NULL,
    title_b TEXT NOT NULL
);

-- The full-text search table
CREATE virtual TABLE pages_fts USING FTS5(
    title,
    body,
    content='pages'
);

-- Before a page is inserted into the pages table,
-- delete the old matching entry in the FTS table
CREATE TRIGGER pages_before_insert BEFORE INSERT ON pages
BEGIN
    INSERT INTO pages_fts (pages_fts, rowid, title, body)
        SELECT 'delete', rowid, title, body
        FROM pages
        WHERE title = new.title
        ORDER BY revision
        DESC
        LIMIT 1;
END;

-- After a page is inserted into the pages table,
-- insert a matching entry into the FTS table
CREATE TRIGGER pages_after_insert AFTER INSERT ON pages
BEGIN
    INSERT INTO pages_fts (rowid, title, body)
    VALUES (new.rowid, new.title, new.body);
END;

-- After a page is deleted from the pages table,
-- delete the matching entry from the FTS table
CREATE TRIGGER pages_after_delete AFTER DELETE ON pages
BEGIN
    INSERT INTO pages_fts (pages_fts, rowid, title, body)
    VALUES ('delete', old.rowid, old.title, old.body);
END;
