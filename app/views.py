# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request
from jinja2  import TemplateNotFound
import os
import secrets
from PIL import Image
from flask import render_template , url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# App modules
from app import app

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})

@app.route('/<path>')
def index(path):

    try:

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( path, segment=segment )
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  

@app.route("/")
def indexpage():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("index.html",posts=posts,title='Home')


@app.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("home.html",posts=posts,title='Home')
    


@app.route("/register", methods=['GET','POST'])
def register():
    """if current_user.is_authenticated:
        return redirect(url_for('index'))"""
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'your account has been created you are now able to login','success')

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    """if current_user.is_authenticated:
        return redirect(url_for('index'))"""
    form = LoginForm()
    if form.validate_on_submit():
        user =  User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:   
            flash('Login Unsucessfull,Please check username and password','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.username.email = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file )    
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created!','success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post', form=form, legend='New post')



@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) 
    return render_template('post.html', title='post.title', post=post)   

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('your post has been updated!','success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.title.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='update post')

@app.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('your post has been deleted!','success')
    return redirect(url_for('index'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template("user_posts.html",posts=posts, user=user, title='Posts')






