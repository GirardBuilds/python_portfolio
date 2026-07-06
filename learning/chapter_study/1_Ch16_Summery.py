Connecting to a Database — sqlite3.connect()
What it is: SQLite stores an entire database in a single file on disk. sqlite3.connect() opens (or creates, if it doesn't exist) that file and returns a Connection object, which is your gateway to running queries against it.
Why it matters: Unlike Excel or CSV, a database lets you run complex, filtered, sorted queries on huge amounts of data without loading everything into memory or writing your own search logic.
Example:
pythonimport sqlite3

conn = sqlite3.connect('example.db', isolation_level=None)
# creates example.db if it doesn't already exist

conn.close()   # call when finished
Gotcha: isolation_level=None puts the connection in autocommit mode, so each query is saved immediately — without it, you'd need to manually call conn.commit() after every change or your data won't actually be saved.

Creating Tables — CREATE TABLE
What it is: A database file can contain multiple tables, and each table stores one kind of record with a fixed set of typed columns. You create a table by passing a CREATE TABLE SQL string to conn.execute(), defining each column's name and data type inside parentheses.
Why it matters: Tables give your data a strict, predictable shape — this structure is what makes fast, reliable querying possible, unlike a spreadsheet where any cell can hold anything.
SQLite data types at a glance:

NULL — like Python's None
INTEGER — like Python's int
REAL — like Python's float
TEXT — like Python's str
BLOB — raw binary data (like Python's bytes)

Example:
pythonconn.execute('''CREATE TABLE IF NOT EXISTS cats
    (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT''')
Gotcha: Without IF NOT EXISTS, running the same CREATE TABLE query twice raises an error. Without the STRICT keyword, SQLite won't enforce column data types at all — it will silently accept a string in a numeric column.

CRUD Operations — INSERT, SELECT, UPDATE, DELETE
What it is: CRUD stands for Create, Read, Update, Delete — the four fundamental things you do with database data. In SQL these map directly to four statement types.
Why it matters: Nearly every app you use is a CRUD interface over a database — learning these four statements covers the vast majority of what databases are used for.
Statements at a glance:

INSERT INTO table VALUES (...) — adds a new row
SELECT ... FROM table — reads rows
UPDATE table SET col = value WHERE ... — modifies existing rows
DELETE FROM table WHERE ... — removes rows

Example:
pythonconn.execute('INSERT INTO cats VALUES ("Zophie", "2021-01-24", "black", 5.6)')

conn.execute('SELECT * FROM cats').fetchall()
# [('Zophie', '2021-01-24', 'black', 5.6)]

conn.execute('UPDATE cats SET fur = "gray tabby" WHERE rowid = 1')

conn.execute('DELETE FROM cats WHERE rowid = 1')
Gotcha: UPDATE and DELETE without a WHERE clause apply to every row in the table — always double-check you have a WHERE clause, or use WHERE 1 deliberately if you really mean to affect all rows.

Preventing SQL Injection — The ? Placeholder
What it is: Instead of inserting Python variables directly into a query string with an f-string, you use ? as a placeholder in the query and pass the actual values as a separate list argument to .execute().
Why it matters: Building queries by directly formatting variables into a string opens the door to SQL injection attacks, where malicious input can change what the query does — the ? syntax prevents this by handling escaping safely.
Example:
python# Risky — don't do this
conn.execute(f'INSERT INTO cats VALUES ("{name}", "{bday}", "{fur}", {weight})')

# Safe
conn.execute('INSERT INTO cats VALUES (?, ?, ?, ?)', [name, bday, fur, weight])
Gotcha: The ? placeholders must be passed a list (or tuple) as the second argument to .execute() — not concatenated or formatted into the string itself.

Reading Data — SELECT, fetchall(), and Looping
What it is: SELECT retrieves rows from a table. Calling .fetchall() on the result pulls everything into a list of tuples at once; alternatively, you can iterate directly over the execute() result in a for loop without loading everything into memory first.
Why it matters: fetchall() is convenient for small result sets, but direct iteration is more memory-efficient for large tables since it processes one row at a time.
Example:
pythonconn.execute('SELECT * FROM cats').fetchall()
# [('Zophie', '2021-01-24', 'black', 5.6), ...]

conn.execute('SELECT rowid, name FROM cats').fetchall()
# [(1, 'Zophie'), ...]  — only requested columns

# Iterate directly (memory-efficient)
for row in conn.execute('SELECT * FROM cats'):
    print(row[0], 'is one of my favorite cats.')
Gotcha: SELECT * returns all columns except rowid — you must explicitly request rowid if you need each row's unique identifier.

Filtering with WHERE
What it is: A WHERE clause added to SELECT, UPDATE, or DELETE restricts which rows are affected, based on a condition. SQLite supports comparison operators similar to Python's (=, !=, <, >, AND, OR), plus pattern-matching operators for partial text matches.
Why it matters: Without filtering, you'd have to pull every row into Python and filter manually — WHERE lets the database do that work far more efficiently.
Pattern-matching operators at a glance:

LIKE — case-insensitive match, % is the wildcard
GLOB — case-sensitive match, * is the wildcard

Example:
pythonconn.execute('SELECT * FROM cats WHERE fur = "black"').fetchall()

conn.execute('SELECT * FROM cats WHERE fur = "black" OR birthdate >= "2024-01-01"').fetchall()

conn.execute('SELECT name FROM cats WHERE name LIKE "%y"').fetchall()   # ends with 'y'
conn.execute('SELECT name FROM cats WHERE name LIKE "Ja%"').fetchall()  # starts with 'Ja'
conn.execute('SELECT name FROM cats WHERE name GLOB "*m*"').fetchall()  # case-sensitive 'm'
Gotcha: SQLite uses = for equality (not == like Python) — using == in a query silently causes a syntax error or unexpected behavior.

Sorting and Limiting — ORDER BY and LIMIT
What it is: ORDER BY sorts query results by one or more columns, ascending by default (ASC) or descending if you add DESC. LIMIT restricts how many rows are returned — done at the database level rather than slicing the result afterward in Python.
Why it matters: Sorting and limiting inside the query is much faster than fetching everything and processing it in Python, especially for large tables.
Example:
pythonconn.execute('SELECT * FROM cats ORDER BY fur').fetchall()

# Multi-column sort
conn.execute('SELECT * FROM cats ORDER BY fur, birthdate').fetchall()

# Descending order
conn.execute('SELECT * FROM cats ORDER BY fur ASC, birthdate DESC').fetchall()

# Limit results
conn.execute('SELECT * FROM cats LIMIT 3').fetchall()   # first 3 rows only
Gotcha: Clause order matters — WHERE must come before ORDER BY, and ORDER BY must come before LIMIT. Writing them out of order raises a syntax error.

Indexes — Speeding Up Searches
What it is: An index is a separate data structure SQLite builds for a specific column to make WHERE lookups on that column much faster. It costs extra storage and slightly slows down inserts/updates on that column, but dramatically speeds up reads.
Why it matters: Worth using on large tables where you filter or search by a column often — not worth the overhead on small tables or write-heavy tables.
Example:
pythonconn.execute('CREATE INDEX idx_name ON cats (name)')

# List indexes
conn.execute('SELECT name FROM sqlite_schema WHERE type = "index" AND tbl_name = "cats"').fetchall()

# Remove an index
conn.execute('DROP INDEX idx_name')
Gotcha: Indexes speed up reads but slow down writes — adding them to a table you update frequently can hurt more than help. Test before assuming an index improves performance.

Transactions — commit() and rollback()
What it is: A transaction is a group of queries treated as one unit. In autocommit mode each query commits instantly, but you can start a manual transaction with BEGIN, then either commit() to save all changes or rollback() to undo everything since the transaction began.
Why it matters: Lets you safely try a batch of changes and back out cleanly if something goes wrong partway through, rather than ending up with half-applied data.
Example:
pythonconn.execute('BEGIN')
conn.execute('INSERT INTO cats VALUES ("Socks", "2022-04-04", "white", 4.2)')
conn.execute('INSERT INTO cats VALUES ("Fluffy", "2022-10-30", "gray", 4.5)')

conn.rollback()   # undoes both inserts — as if they never happened
# or
conn.commit()     # makes both inserts permanent
Gotcha: rollback() only undoes changes made since the last BEGIN — it can't undo anything that's already been committed.

Backing Up Databases
What it is: If no program is actively using the database file, you can back it up with a simple file copy (shutil.copy()). If the database is actively being read or written, use the Connection object's .backup() method instead, which safely copies data even while queries are running.
Why it matters: Protects you from data loss due to bugs, accidental bad queries, or crashes — always have a way to restore to a known-good state.
Example:
pythonimport sqlite3

conn = sqlite3.connect('sweigartcats.db', isolation_level=None)
backup_conn = sqlite3.connect('backup.db', isolation_level=None)
conn.backup(backup_conn)
Gotcha: A plain file copy (shutil.copy()) is unsafe while the database is actively being written to — you can end up with a corrupted or partial copy. Use .backup() for databases in active use.

Altering and Dropping Tables — ALTER TABLE, DROP TABLE
What it is: ALTER TABLE lets you rename a table, rename a column, or add/remove columns after the table already exists. DROP TABLE deletes an entire table and all its data permanently.
Why it matters: Schemas evolve — you'll eventually need to adjust table structure without recreating the whole database from scratch.
Statements at a glance:

ALTER TABLE old RENAME TO new — renames a table
ALTER TABLE t RENAME COLUMN old TO new — renames a column
ALTER TABLE t ADD COLUMN col TYPE — adds a new column
ALTER TABLE t DROP COLUMN col — removes a column and its data
DROP TABLE t — deletes the entire table

Example:
pythonconn.execute('ALTER TABLE cats RENAME TO felines')
conn.execute('ALTER TABLE felines RENAME COLUMN fur TO description')
conn.execute('ALTER TABLE felines ADD COLUMN is_loved INTEGER DEFAULT 1')
conn.execute('ALTER TABLE felines DROP COLUMN is_loved')

conn.execute('DROP TABLE felines')   # deletes everything — no undo
Gotcha: DROP TABLE and DROP COLUMN permanently delete data with no confirmation prompt — always back up first.

Foreign Keys and Joins — Linking Tables
What it is: A foreign key is a column in one table that stores the rowid of a row in another table, creating a link between related records across tables. An INNER JOIN query combines matching rows from both tables into a single result set.
Why it matters: Lets you model one-to-many relationships (like one cat having multiple vaccination records) without cramming a variable number of columns into a single table.
Example:
pythonconn.execute('PRAGMA foreign_keys = ON')   # enable foreign key enforcement

conn.execute('''CREATE TABLE IF NOT EXISTS vaccinations
    (vaccine TEXT, date_administered TEXT, administered_by TEXT,
     cat_id INTEGER, FOREIGN KEY(cat_id) REFERENCES cats(rowid)) STRICT''')

conn.execute('INSERT INTO vaccinations VALUES ("rabies", "2023-06-06", "Dr. Echo", 1)')

# Join cats with their vaccination records
conn.execute('''SELECT * FROM cats
    INNER JOIN vaccinations ON cats.rowid = vaccinations.cat_id''').fetchall()
Gotcha: Foreign key enforcement is off by default in SQLite — you must run PRAGMA foreign_keys = ON after every connection, or invalid references (like a cat_id that doesn't exist) will be silently allowed.

In-Memory Databases
What it is: Instead of a file, you can create a database that lives entirely in RAM by passing ':memory:' as the filename to sqlite3.connect(). This makes queries extremely fast, but the data disappears when the program ends unless you explicitly back it up to a file.
Why it matters: Useful for temporary, high-speed processing where persistence isn't needed until the very end, or for testing.
Example:
pythonmem_conn = sqlite3.connect(':memory:', isolation_level=None)
mem_conn.execute('CREATE TABLE test (name TEXT, number REAL)')
mem_conn.execute('INSERT INTO test VALUES ("foo", 3.14)')

# Save to disk before the program ends
file_conn = sqlite3.connect('test.db', isolation_level=None)
mem_conn.backup(file_conn)
Gotcha: If your program crashes before you call .backup(), the entire in-memory database is lost — just like any other variable in memory.

Summary:

sqlite3.connect(filename, isolation_level=None) gets a Connection; conn.execute(query) runs SQL strings; .close() when done
CREATE TABLE IF NOT EXISTS defines a table's structure; use STRICT mode to enforce column data types
CRUD maps to INSERT, SELECT, UPDATE, DELETE — always include a WHERE clause on UPDATE/DELETE to avoid modifying every row
Use ? placeholders with a list of values instead of building query strings with f-strings — avoids SQL injection
fetchall() loads all results into a list of tuples; iterating execute() directly is more memory-efficient for large tables
WHERE, ORDER BY, and LIMIT must appear in that order in a query — filtering and sorting are faster done in SQL than in Python
Indexes speed up reads on frequently-searched columns at the cost of slightly slower writes
Transactions (BEGIN / commit() / rollback()) let you group and safely undo batches of changes
.backup() safely copies an actively-used database; ALTER TABLE / DROP TABLE modify or remove schema — always back up first
Foreign keys link related tables together; PRAGMA foreign_keys = ON must be set explicitly to enforce referential integrity
':memory:' creates a fast, RAM-only database — remember to .backup() it to a file before the program exits
