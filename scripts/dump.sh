#!/usr/bin/env sh

echo BEGIN;

sqlite3 instance/silicon.sqlite << EOF
.mode insert pages
SELECT * FROM pages;

.mode insert relationships
SELECT * FROM relationships;
EOF

echo COMMIT;
