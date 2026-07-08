'''
Drill 2 — Write most_recent_review(user_id)
a function that returns the single most recent review a user has made
(the actual row: card_id, result, reviewed_at), or None if theyve never reviewed anything.

What table, what column are you filtering by — same as before.

You dont want all their reviews, just the newest one.

Is there a SQL keyword that lets you sort rows by a column before returning them
you've actually seen this exact keyword already, sitting inside db_Copy.py's own pick_next_card() function,
sorting by due_date.

Whats it called, and which direction (ASC or DESC)
would put the newest timestamp first, given reviewed_at is stored as a sortable ISO string?

Once sorted newest-first, you only want the single top result,
not the whole list.

Is there a keyword that caps how many rows come back
same one you also saw already, in that same pick_next_card() function?

Given you want one row or nothing, is .fetchone() or .fetchall() the correct call at the end?
'''

SCHEMA = """
CREATE TABLE IF NOT EXISTS reviews (
    review_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    card_id    INTEGER NOT NULL,
    result     TEXT NOT NULL,          -- got_it | missed | skip
    reviewed_at TEXT NOT NULL
);
"""



def most_recent_review(user_id: int):
    with conn() as c:
        row = c.execute(
            """SELECT * FROM reviews WHERE user_id =? ORDER BY reviewed_at DESC LIMIT 1""",
            (user_id,),
        ).fetchone()
    if row is None:
        return None
    return row









