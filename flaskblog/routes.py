import secrets
import os
from PIL import Image
from flaskblog.models import User, Post
from flask import  request,render_template,url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


def add_user_to_db(user):
	db.session.add(user)
	db.session.commit()

def create_user(form):
	hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
	user = User(username=form.username.data,email=form.email.data,password=hashed_password)
	add_user_to_db(user)


@app.route("/home")
@app.route("/")
def home():
	posts = Post.query.all()
	return render_template('home.html',posts=posts)


@app.route("/about")
def about():
	return render_template('about.html',title="About")


@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	registration_form = RegistrationForm()
	if registration_form.validate_on_submit():
		create_user(registration_form)
		flash(f'Account created!','success')
		return redirect(url_for('login'))
	return render_template('register.html',title="register",form=registration_form)

def is_this_user_in_the_db(form,user):

	return user and bcrypt.check_password_hash(user.password,form.password.data)

@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	login_form = LoginForm()
	if login_form.validate_on_submit():
		user = User.query.filter_by(email=login_form.email.data).first()

		if  is_this_user_in_the_db(login_form,user):
			login_user(user,remember=login_form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else (url_for('home'))
		else:
			flash(f'Login unsuccessfull. check email and password ','danger')

	return render_template('login.html',title="login",form=login_form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

def update_user_account(form):
	current_user.username = form.username.data
	current_user.email = form.email.data
	db.session.commit()

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex+f_ext
	picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
	output_size = (125,125)
	image = Image.open(form_picture)
	image.thumbnail(output_size)

	image.save(picture_path)
	return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		update_user_account(form)
		flash('Account has benn updated!' ,'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
	return render_template('account.html',title='Account',image_file=image_file, form=form)

@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data,content=form.content.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('your post has been created ','success')
		return redirect(url_for('home'))
	return render_template('create_post.html',title='Title',form=form)
