"""
Model functions for managing page relationships.
"""

from flask import current_app
from slugify import slugify

from silicon.db import get_db


def get(title):
    """
    Get page relationships.

    Returns a sequence of pages (by title) related to `title`.
    """
    c = get_db()
    c.row_factory = None
    rels = c.execute(
        "SELECT title_b FROM relationships WHERE title_a = ? "
        "UNION ALL "
        "SELECT title_a FROM relationships WHERE title_b = ?",
        (title, title)
        ).fetchall()
    return sorted([r[0] for r in rels])


def add(title, related):
    """
    Add a relationship between pages.

    The string for `related` is limited to 80 chars mainly to defend against
    accidentally pasting a whole Shakespeare manuscript into it.
    """

    related_slug = slugify(related, separator="_", max_length=80)

    if len(related_slug) == 0:
        current_app.logger.info(f"got empty string for {title} relative")
        return

    if title == related_slug:
        current_app.logger.info(f"{title} cannot be related to itself")
        return

    rels = get(title)
    if related in rels:
        current_app.logger.info(
            f"duplicate relationship: {title}, {related_slug}"
        )
        return

    try:
        db = get_db()
        db.execute(
            "INSERT INTO relationships VALUES (?, ?)",
            (title, related_slug)
        )
        db.commit()
    except Exception as err:
        current_app.logger.critical(f"Error saving relationship: {err}")


def delete(title, related):
    """
    Delete a relationship between pages.
    """

    rels = get(title)
    if related not in rels:
        current_app.logger.info(
            f"relationship doesn't exist: {title}, {related}"
        )
        return

    try:
        db = get_db()
        db.execute(
            "DELETE FROM relationships WHERE "
            "(title_a = ? and title_b = ?) "
            "OR "
            "(title_b = ? and title_a = ?)",
            (title, related, title, related)
        )
        db.commit()
    except Exception as err:
        current_app.logger.critical(f"Error deleting relationship: {err}")
