'''
Drill 1 — Open database_Copy.py and find the SCHEMA string.
Pick the cards table specifically. Without running anything,
answer in plain English: what are this tables column names,
and what Python values would you need on hand to insert one new row into it?
'''
SCHEMA = """
CREATE TABLE IF NOT EXISTS cards (
    card_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    deck_id    INTEGER NOT NULL REFERENCES decks(deck_id),
    front      TEXT NOT NULL,
    back       TEXT NOT NULL,
    created_at TEXT NOT NULL
);
--------------------------------------------------------------------------------------------------------------------------------------------------
if the table named cards doesnt exist create one with the following columns (or add to one with the appropriate data):
header:    card_id , deck_id, front, back, created_at
row 1:  integer(auto enumerate), integer(not None)needs to be handed deck deck_id in callout , string(not None),string(not None), string(not None)
--------------------------------------------------------------------------------------------------------------------------------------------------

Theres no existing function in db_Copy.py that does this,
so youll build it from the ground up: write a function count_reviews_for_user(user_id)
that returns how many rows exist in reviews for a given user,
regardless of whether the result was got_it, missed, or skip.

Before writing Python — write just the raw SQL string in plain English first:

what table are you selecting from, what column are you filtering by,

and — since you want a count,
not the actual rows — is there a SQL keyword that counts matching rows for you,
rather than you fetching everything and counting it yourself in Python?
(You've actually already seen this exact keyword used, more than once, inside database_Copy.py's own stats() function —
go look at how totals gets built, right near the top of stats().)

Now the real drill — writing a query from scratch, no existing function to model.
Look at the reviews table in SCHEMA:
"""
SCHEMA = """
CREATE TABLE IF NOT EXISTS reviews (
    review_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    card_id    INTEGER NOT NULL,
    result     TEXT NOT NULL,
    reviewed_at TEXT NOT NULL
);
"""


def count_reviews_for_user(user_id: int):
    with conn() as c:
        result = c.execute(
            "SELECT COUNT(*) AS total FROM reviews WHERE user_id=?",
            (user_id,)
        ).fetchone()
    return result['total']

APS = as per schema

function takes user id number as int (APS)
conects the database
result is a comand executed to count the total rows from the reviews section within the user_id number section
=? means it only pulls data from the following tupple then fetching the number from the command
returning the result ['total'] (APS' AS total') number instead of the sqlite3.row object
















