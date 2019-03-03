from flaskblog.models import User, Post
from flask import  request,render_template,url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
posts = [
	{
	'author':'Alex',
	'title':'Blog post 1',
	'content':'First post content',
	'date_posted':'28/02/2019'
	},
	{
	'author':'Juan',
	'title':'Blog post 2',
	'content':'Seconds post content',
	'date_posted':'28/02/2019'
	}
]

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


@app.route("/account")
@login_required
def account():
	return render_template('account.html',title='Account')
