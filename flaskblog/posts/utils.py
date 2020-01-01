import bleach
from markdown import markdown
from flask import Markup
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension


def render_post_content(content):
    allowed_tags = ['h1', 'h2', 'h3', 'div', 'p', 'code', 'table', 'span',
                    'pre', 'tr', 'td', 'tbody']
    allowed_attributes = {'*': ['id', 'class']}
    html = markdown(content, extensions=[CodeHiliteExtension(
        linenums=True), FencedCodeExtension()])
    html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes)
    html = Markup(html)
    return html
