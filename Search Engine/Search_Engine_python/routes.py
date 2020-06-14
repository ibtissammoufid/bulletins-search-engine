from flask import render_template, url_for, flash, redirect, request
from Search_Engine_python import app, db, bcrypt
from Search_Engine_python.forms import RegistrationForm, LoginForm
from Search_Engine_python.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

from elasticsearch import Elasticsearch
import os
os.chdir("C:\\Users\\hp\\Desktop\\Search Engine\\")

es = Elasticsearch('127.0.0.1', port=9200)
es = Elasticsearch(timeout=30)




@app.route('/')
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/search")
def search():
    return render_template('search.html')

@app.route('/results', methods=['GET', 'POST'])
def request_search():
    search_term = request.form["input"]
    res = es.search(
        index='bulletins',
        body={
            "query": {"match_phrase": {"content": search_term}},
            "highlight": {"pre_tags": ["<b>"], "post_tags": ["</b>"], "fields": {"content": {}}}})
    res['ST'] = search_term
    for hit in res['hits']['hits']:
        hit['good_summary'] = '….'.join(hit['highlight']['content'][1:])
    return render_template('results.html', res=res)






@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('search'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))





@app.route("/saved")
def saved():
    posts = Post.query.filter_by(author=current_user)

    return render_template('saved.html', posts=posts)

@app.route("/results/<post_name>/<post_path>/add", methods=['GET', 'POST'])
@login_required
def newpost(post_name, post_path):
    post = Post(title=post_name, content=post_path, author=current_user)
    db.session.add(post)
    db.session.commit()
    posts = Post.query.all()
    for post in posts :
        if post.content == 'f':
            db.session.delete(post)
        db.session.commit()
    flash('Your post has been created!', 'success')
    return redirect(url_for('saved'))


