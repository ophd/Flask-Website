import bleach
from markdown import markdown
from bs4 import BeautifulSoup
from flask import Markup, Blueprint
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension

posts_utils = Blueprint('posts_utils', __name__)


@posts_utils.app_context_processor
def utility_processor():
    def render_post_content(content, first_paragraph=False):
        allowed_tags = ['h1', 'h2', 'h3', 'div', 'p', 'code', 'table', 'span',
                        'pre', 'tr', 'td', 'tbody']
        allowed_attributes = {'*': ['id', 'class']}
        html = markdown(content, extensions=[CodeHiliteExtension(
            linenums=True), FencedCodeExtension()])
        html = bleach.clean(html, tags=allowed_tags,
                            attributes=allowed_attributes)
        soup = BeautifulSoup(html, 'html.parser')
        if first_paragraph:
            html = soup.p
        html = Markup(html)
        return html

    return dict(render_post_content=render_post_content)
