from flask import render_template, redirect, flash, request, url_for, Blueprint
from flaskblog.users.forms import (UserRegistrationForm,
                            UserLoginForm, UserUpdateAccountForm,
                            RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flaskblog import bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_picture, send_reset_email

users= Blueprint('users', __name__)


#Create Registration route
@users.route('/register', methods= ['GET', 'POST'])
def register():
    form= UserRegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user= User(username= form.username.data, email= form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'You are successfully registered, you can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title= 'Register', form= form)



#Create login route
@users.route('/login', methods= ['POST', 'GET'])
def login():
    form= UserLoginForm()
    if current_user.is_authenticated:
        return redirect('home')
    if form.validate_on_submit():
        user= User.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            next_page= request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Your username or password does not match!', 'danger')
    return render_template('login.html', title= 'Login', form= form)



@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route('/account', methods=['POST', 'GET'] )
@login_required
def account():
    form= UserUpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file= save_picture(form.picture.data)
            current_user.image_file= picture_file
        current_user.username= form.username.data
        current_user.email= form.email.data
        db.session.commit()
        flash('Your account has been updated successifully!', 'success')
        return redirect(url_for('users.account'))
    elif request.method== 'GET':
        form.username.data= current_user.username
        form.email.data= current_user.email

    image_file= url_for('static', filename= f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title= 'Account', image_file= image_file, form= form)




#Create a route for every user posts
@users.route('/user/<string:username>/')
def user_posts(username):
    page= request.args.get('page', 1, type= int)
    user= User.query.filter_by(username= username).first_or_404()
    posts= Post.query.filter_by(author= user).order_by(Post.date_posted.desc()).paginate(page= page, per_page= 2)
    return render_template('user_posts.html', posts= posts, user= user)



# create a route for password request
@users.route('/password_reset', methods= ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form= RequestResetForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email= form.email.data)
        send_reset_email(user)
        flash('The email has been send with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title= 'Password Reset', form= form)

# create a route for them to finally reset their password
@users.route('/password_reset/<token>/', methods= ['GET', 'POST'])
def request_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user= User.verify_reset_token(token)
    if user is None:
        flash('That token is invalid or expired', 'warning')
        return redirect(url_for('users.reset_request'))
    form= ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password= hashed_password
        db.session.commit()
        flash('Your password is updated successfully, you can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title= 'password Reset', form= form)
