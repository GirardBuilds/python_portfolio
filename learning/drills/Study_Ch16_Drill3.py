"""
Drill 3 — the JOIN.

The problem: reviews only stores card_id — a bare number.
If you want to know what the question actually said for someone's most recent review,
reviews alone can't tell you; you'd need to also look inside cards,
matching reviews.card_id to cards.card_id, to pull the front/back text.
That's what a JOIN is for — stitching two tables together, row-to-row, wherever a shared key matches.
"""

Write the complete query — SELECT your three target columns
(result, reviewed_at from reviews; front from cards),

FROM reviews, JOIN cards ON the fully-qualified match condition, WHERE user_id=? unprefixed. Then the full Python function using conn(),
.execute() with the parameter tuple, and .fetchall() since you want every matching row back, not just one.


def reviews_with_card_text(user_id: int):
    with conn() as c:
        return c.execute(
        """SELECT reviews.result, reviews.reviewed_at, cards.front
           FROM reviews LEFT JOIN cards ON cards.card_id = reviews.card_id
           WHERE reviews.user_id=? """,
            (user_id,),
        ).fetchall()

select within the reviews table the result and reviewed_at then select within the cards table the front of the cards
from the reviews table left side of the columns? joint



























