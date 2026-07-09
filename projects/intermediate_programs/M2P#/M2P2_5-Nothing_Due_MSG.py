"""
M2P2.5 - the ready to advance/add cards messege
The goal is one message per day maximum, only when a ping would otherwise be silent.
The work happens entirely inside send_ping's if card is None: branch.
You need to remember one fact per user — "when did I last send them a caught-up notice" —
and the honest place for that is the database, since it must survive restarts:

add a column to the users table (nullable text, e.g. last_caught_up),
which for an existing database means

running one ALTER TABLE users ADD COLUMN... against it once,

plus adding the column to the schema in db.py so fresh databases get it too.

Then the branch logic reads: fetch the user's last_caught_up; if it's empty or more than 24 hours ago,

send "You're all caught up ✅ — nothing due right now" and write the current timestamp back;

otherwise stay silent as before. Two small helper functions in db.py
(a getter and a setter, following the exact shape of set_frequency) keep the SQL out of bot.py.
That's the whole feature: one column, two helpers, one if-block.

The one gotcha flagged alongside it:
    compare timestamps as datetime objects, not strings — parse with the same ISO format string db.py already uses everywhere.
"""

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id       INTEGER PRIMARY KEY,        -- telegram user id
    chat_id       INTEGER NOT NULL,
    username      TEXT,
    pings_per_day INTEGER NOT NULL DEFAULT 4,
    wake_start    INTEGER NOT NULL DEFAULT 9,   -- hour, 24h clock
    wake_end      INTEGER NOT NULL DEFAULT 21,
    paused        INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT NOT NULL,
    last_caught_up TEXT
);"""


#Added to db copy

def get_last_caught_up(user_id: int,):
    with conn() as c:
        return c.execute("SELECT last_caught_up FROM users WHERE user_id=?", (user_id,)).fetchone()


def set_last_caught_up(user_id:int):
    with conn() as c:
        c.execute("UPDATE users SET last_caught_up=? WHERE user_id=?", (datetime.now().strftime(ISO), user_id))

#Added to bot copy

if card is None:
        value = db_Copy.get_last_caught_up(user_id)
        value = value['last_caught_up']
        if value is None:
            pass
        else:
            dt = datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
            time_diff = datetime.now() - dt
            if time_diff.days > 1:
                return
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"You're all caught up ✅ — nothing due right now",)
        db_Copy.set_last_caught_up(user_id)
        return  # nothing due and no new cards; stay silent rather than nag





















