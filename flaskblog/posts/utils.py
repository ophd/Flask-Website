from markdown import markdown
from flask import Markup
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension

def render_post_content(content):
    html = markdown(content, extensions=[CodeHiliteExtension(linenums=True), FencedCodeExtension()])
    html = Markup(html)
    return html