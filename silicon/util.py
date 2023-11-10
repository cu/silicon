from slugify import slugify


def slugify_title(title):
    """
    Consistently slugify article titles.

    Limited to 80 chars mainly to defend against accidentally pasting a whole
    Shakespeare manuscript into it.
    """
    return slugify(title, separator='_', max_length=80)
