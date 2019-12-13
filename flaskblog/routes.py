from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm

posts = [
    {
        'author':   'Olivier Daigle',
        'title':    'Blog Post 1',
        'content':  'First post content.',
        'date_posted': '5 December 2019'
    },
    {
        'author':   'Olivier Daigle',
        'title':    'Blog Post 2',
        'content':  'Second post content.',
        'date_posted': '6 December 2019'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have logged in successfully!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check username and password', category='danger')

    return render_template('login.html', title='Login', form=form)