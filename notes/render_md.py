from flask import url_for
import mistune
from mistune.directives import render_toc_ul
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
from slugify import slugify

"""
In this module, we add these extra features to mistune:

* Syntax highlighting in code blocks.
* Wiki-style links, via a custom plugin inspired by the mistune docs.
* Heading `id` with slugified text.
* A table of contents renderer.
"""


class CustomRenderer(mistune.HTMLRenderer):
    """
    Customized Mistune renderer to add the following features:

    * Highlighted code blocks
    * `rel` attribute in external links
    """

    def block_code(self, text, lang=None):
        """Renderer for syntax highlighting of code blocks."""

        html = '<pre><code>' + mistune.escape(text) + '</code></pre>\n'

        if lang:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except ClassNotFound:
                return html
            else:
                formatter = HtmlFormatter()
                return highlight(text, lexer, formatter)

        return html

    def link(self, link, text=None, title=None):
        """Renderer for external links.

        This is customized from the mistune renderer to add the `rel` attribute.
        """

        if text is None:
            text = link

        s = '<a rel="external noreferrer" href="' + self._safe_url(link) + '"'
        if title:
            s += ' title="' + mistune.escape_html(title) + '"'
        return s + '>' + (text or link) + '</a>'

    def heading(self, text, level):
        """Return heading HTML with slugified text in the `id` attribute.

        todo: paragraph link thing
        """

        level = str(level)
        return f'<h{level} id="{slugify(text)}">{text}</h{level}>\n'


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
    """Render a Markdown document into HTML."""

    markdown = mistune.create_markdown(
        renderer=CustomRenderer(escape=False),
        plugins=[
            'strikethrough',
            'footnotes',
            'table',
            'url',
            'def_list',
            'abbr',
            wiki_links,
        ]
    )
    return markdown(text)


def ast_renderer(text):
    """Render a Makrdown document into an Abstract Syntax Tree."""

    ast = mistune.create_markdown(renderer=mistune.AstRenderer())
    return ast(text)


def walk_heading_children(ast):
    """
    Headings are block-level elements but can have inline markup as child
    nodes.
    """

    text = ''
    for node in ast:
        if 'children' in node:
            text += walk_heading_children(node['children'])
        if 'text' in node:
            text += node['text']
    return text


def toc_renderer(text):
    """Render a Markdown document into an HTML table of contents."""

    ast = ast_renderer(text)
    headings = []

    # walk the AST to find headings, calling walk_heading_children() if any
    # headings have child nodes
    for node in ast:
        text = ''
        if node['type'] == 'heading':
            text += mistune.escape_html(walk_heading_children(node['children']))
            headings.append((slugify(text), text, node['level']))

    return render_toc_ul(headings)
