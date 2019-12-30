from flask import render_template,  request, Blueprint
from flaskblog.models import Post
from flaskblog.posts.utils import render_post_content


main = Blueprint('main', __name__)


@main.route('/home')
@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(per_page=10, page=page)

    return render_template('home.html', posts=posts,
                render_post_content=render_post_content)


@main.route('/about')
def about():
    return render_template('about.html', title='About')
