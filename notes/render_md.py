import re

from flask import url_for
from mistune import escape, Markdown, Renderer, InlineGrammar, InlineLexer
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from slugify import slugify


"""
In this module, we add two "extra" features to mistune:

1. Syntax highlighting in code blocks.
2. Wiki-style links, via a custom mixin inspired by the mistune README.
"""


class HighlightMixin(object):
    def block_code(self, text, lang):
        inlinestyles = self.options.get('inlinestyles', False)
        linenos = self.options.get('linenos', False)

        if not lang:
            text = text.strip()
            return u'<pre><code>%s</code></pre>\n' % escape(text)

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(
                noclasses=inlinestyles, linenos=linenos
            )
            code = highlight(text, lexer, formatter)
            if linenos:
                return '<div class="highlight-wrapper">%s</div>\n' % code
            return code
        except:
            return '<pre class="%s"><code>%s</code></pre>\n' % (
                lang, escape(text)
            )


class WikiLinkMixin():
    def wiki_link(self, alt, page):
        """
        Render link as HTML
        """
        link = url_for('page.view', title=page)
        return f'<a class="internal-link" href="{link}">{alt}</a>'


class WikiLinkInlineLexer(InlineLexer):
    def __init__(self, renderer, rules=None, **kwargs):
        super().__init__(renderer, rules, **kwargs)

    def enable_wiki_link(self):
        # add wiki_link rules
        self.rules.wiki_link = re.compile(
            r'\[{2}'                            # [[
            r'([\w `~!@#$%^&*()\-=+|:\'",./?\{\}]+?)'    # link text
            r'\]{2}'                            # ]]
        )
        self.default_rules.insert(3, 'wiki_link')

    def output_wiki_link(self, m):
        text = m.group(1)
        if '|' in text:
            page, alt = text.split('|', maxsplit=1)
        else:
            page = alt = text
        slug_link = slugify(page, separator='_')
        return self.renderer.wiki_link(alt, slug_link)


class MarkdownRenderer(HighlightMixin, WikiLinkMixin, Renderer):
    pass


def md_renderer(text):
    md = MarkdownRenderer()
    inline_lexer = WikiLinkInlineLexer(md)
    inline_lexer.enable_wiki_link()
    render = Markdown(renderer=md, inline=inline_lexer)
    return render(text)
