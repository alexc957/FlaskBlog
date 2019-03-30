from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
from flaskblog.users.utils import save_picture


users = Blueprint('users',__name__)
def add_user_to_db(user):
	db.session.add(user)
	db.session.commit()

def create_user(form):
	hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
	user = User(username=form.username.data,email=form.email.data,password=hashed_password)
	add_user_to_db(user)


@users.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	registration_form = RegistrationForm()
	if registration_form.validate_on_submit():
		create_user(registration_form)
		flash(f'Account created!','success')
		return redirect(url_for('users.login'))
	return render_template('register.html',title="register",form=registration_form)

def is_this_user_in_the_db(form,user):

	return user and bcrypt.check_password_hash(user.password,form.password.data)

@users.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	login_form = LoginForm()
	if login_form.validate_on_submit():
		user = User.query.filter_by(email=login_form.email.data).first()

		if  is_this_user_in_the_db(login_form,user):
			login_user(user,remember=login_form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash(f'Login unsuccessfull. check email and password ','danger')

	return render_template('login.html',title="login",form=login_form)

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))

def update_user_account(form):
	current_user.username = form.username.data
	current_user.email = form.email.data
	db.session.commit()

@users.route("/account", methods=['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		update_user_account(form)
		flash('Account has benn updated!' ,'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
	return render_template('account.html',title='Account',image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
	page = request.args.get('page',1,type=int)
	user = User.query.filter_by(username=username).first_or_404()


	posts = Post.query.filter_by(author=user)\
			.order_by(Post.date_posted.desc())\
			.paginate(page=page,per_page=5)
	return render_template('user_posts.html',posts=posts,user = user)
