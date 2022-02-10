from datetime import datetime
from html import escape
import re

from flask import Markup


def human_timestamp(timestamp):
    return datetime.fromisoformat(timestamp).strftime('%B %d %Y, %H:%M:%S')


def mark_query_results(snippet):
    """
    A page body might have HTML in it, which we don't want rendered in search
    results. This Jinja filter strips HTML, and then marks matched search terms.

    A page body might have HTML in it. We don't want it rendered in the search
    results because it's effectively noise and we certainly don't want to
    render it here.

    This filter strips HTML tags, escapes any remaining entities, and marks
    (highlights) the matched search terms.
    """

    stripped = escape(Markup(snippet).striptags())
    return re.sub(r'__mark__(.+?)__/mark__', r'<mark>\1</mark>', stripped)
