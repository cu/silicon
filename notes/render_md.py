from flask import url_for
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from slugify import slugify

"""
In this module, we add two extra features to mistune:

1. Syntax highlighting in code blocks.
2. Wiki-style links, via a custom plugin inspired by the mistune docs.
"""


class CustomRenderer(mistune.HTMLRenderer):
    """
    Customized Mistune renderer to add the following features:

    * Highlighted code blocks
    * `rel` attribute in external links
    """


    def block_code(self, text, lang=None):
        """Renderer for syntax highlighting of code blocks."""
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)

        return '<pre><code>' + mistune.escape(text) + '</code></pre>\n'

    def link(self, link, text=None, title=None):
        """Renderer for external links.

        This is customized from the mistune renderer to add the `rel` attribute.
        """

        if text is None:
            text = link

        s = '<a rel="external noreferrer" href="' + self._safe_url(link) + '"'
        if title:
            s += ' title="' + escape_html(title) + '"'
        return s + '>' + (text or link) + '</a>'



def wiki_links(md):
    """Wiki-style links plugin for mistune."""

    def parse_wiki(inline, m, state):
        """
        Parse wiki links.

        `inline` is `md.inline`, see below
        `m` is matched regex item
        """

        text = m.group(1)
        if '|' in text:
            page, title = text.split('|', maxsplit=1)
        else:
            page = title = text
        return 'wiki', slugify(page, separator='_'), title

    def render_html_wiki(page, link_text):
        """Render wiki links as internal links."""

        url = url_for('page.view', title=page)
        return f'<a class="internal-link" href="{url}">{link_text}</a>'

    WIKI_PATTERN = (
        r'\[{2}'                                   # [[
        r'([\w `~!@#$%^&*()\-=+|:\'",./?\{\}]+?)'  # link text
        r'\]{2}'                                   # ]]
    )

    md.inline.register_rule('wiki', WIKI_PATTERN, parse_wiki)

    # add wiki rule into active rules
    md.inline.rules.append('wiki')

    # add HTML renderer
    if md.renderer.NAME == 'html':
        md.renderer.register('wiki', render_html_wiki)


def md_renderer(text):
    markdown = mistune.create_markdown(
        renderer=CustomRenderer(escape=False),
        plugins=[
            'strikethrough',
            'footnotes',
            'table',
            'url',
            'task_lists',
            'def_list',
            'abbr',
            wiki_links
        ]
    )
    return markdown(text)
