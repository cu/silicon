import os
from flask import url_for
from mistune import create_markdown, HTMLRenderer
from mistune.util import safe_entity
from mistune.toc import render_toc_ul
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from slugify import slugify

"""
In this module, we add these extra features to mistune:

* Syntax highlighting in code blocks.
* Wiki-style links, via a custom plugin inspired by the mistune docs.
* Heading `id` with slugified text.
* A table of contents renderer.
"""


class CustomRenderer(HTMLRenderer):
    """
    Customized Mistune renderer to add the following features:

    * Syntax highlighting in code blocks
    * `rel="external noreferrer"` in external links
    * Heading `id` with slugified text.
    """
    def block_code(self, code, info=None):
        """Renderer for syntax highlighting of code blocks.

        This overrides the built-in mistune `block_code()` renderer to use
        pygments syntax highlighting.
        """

        html = f'<pre><code>{self.text(code)}</code></pre>\n'

        if info:
            try:
                lexer = get_lexer_by_name(info, stripall=True)
            except ClassNotFound:
                return html
            else:
                formatter = HtmlFormatter()
                return highlight(code, lexer, formatter)

        return html

    def link(self, text, url, title=None):
        """Renderer for external links.

        This overrides the built-in mistune renderer to add the `rel`
        attribute.
        """
        s = f'<a rel="external noreferrer" href="{self.safe_url(url)}"'
        if title:
            s += f' title="{safe_entity(title)}"'
        return f'{s}>{text}</a>'

    def heading(self, text, level, **attrs):
        """Return heading HTML with slugified text in the `id` attribute.

        todo: paragraph link thing
        """
        level = str(level)
        return f'<h{level} id="{slugify(text)}">{text}</h{level}>\n'


def wiki_links(md):
    """Wiki-style links plugin for mistune."""

    WIKI_PATTERN = (
        r'\[{2}'                                   # [[
        r'(?P<link_text>[\w `~!@#$%^&*()\-=+|:\'",./?\{\}]+?)'  # link text
        r'\]{2}'                                   # ]]
    )

    def parse_wiki(inline, m, state):
        """
        Parse wiki links.

        `inline` is `md.inline`, see below
        `m` is matched regex item
        """

        text = m.group('link_text')
        if '|' in text:
            page, title = text.split('|', maxsplit=1)
        else:
            page = title = text
        page_name = slugify(page, separator='_')
        token = {'type': 'wiki', 'raw': title, 'attrs': {'page': page_name}}
        state.append_token(token)
        return m.end()

    def render_html_wiki(renderer, text, **attrs):
        """Render wiki links as internal links."""

        url = url_for('page.view', title=attrs['page'])
        return f'<a class="internal-link" href="{url}">{text}</a>'

    # Register the wiki link parser
    md.inline.register('wiki', WIKI_PATTERN, parse_wiki, before='link')

    # Register the wiki link renderer
    if md.renderer and md.renderer.NAME == 'html':
        md.renderer.register('wiki', render_html_wiki)


def md_renderer(text):
    """Render a Markdown document into HTML."""

    markdown = create_markdown(
        hard_wrap=(os.getenv('MD_HARD_WRAP') or "").lower() == "true",
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


def toc_renderer(text):
    """Render a Markdown document into an HTML table of contents."""

    def walk_heading_children(ast):
        """
        Headings are block-level elements but can have inline markup as child
        nodes.
        """

        text = ''
        for node in ast:
            if 'children' in node:
                text += walk_heading_children(node['children'])
            if 'raw' in node:
                text += node['raw']
        return text

    ast_renderer = create_markdown(renderer='ast')
    ast = ast_renderer(text)
    headings = []

    # walk the AST to find headings, calling walk_heading_children() if any
    # headings have child nodes
    for node in ast:
        text = ''
        if node['type'] == 'heading':
            text += safe_entity(walk_heading_children(node['children']))
            headings.append((node['attrs']['level'], slugify(text), text))

    return render_toc_ul(headings)
