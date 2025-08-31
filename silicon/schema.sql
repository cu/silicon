CREATE TABLE pages (
    revision TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    PRIMARY KEY (revision, title)
);

-- creating the index should be done after the inserts on bulk import of data
CREATE INDEX pages_idx ON pages (
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

-- After a page is deleted from the pages table,
-- delete the matching entry from the FTS table
CREATE TRIGGER pages_after_delete AFTER DELETE ON pages
BEGIN
    INSERT INTO pages_fts (pages_fts, rowid, title, body)
    VALUES ('delete', old.rowid, old.title, old.body);
END;
