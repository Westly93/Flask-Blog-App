from flask import redirect, url_for, render_template, flash, request, abort, Blueprint
from flaskblog.posts.forms import UserCreatePostForm
from flask_login import current_user, login_required
from flaskblog.models import Post
from flaskblog import db

posts= Blueprint('posts', __name__)


# Create a new post route
@posts.route('/post/new', methods= ['GET', 'POST'])
def create_post():
    form= UserCreatePostForm()
    if form.validate_on_submit():
        post= Post(title= form.title.data, content= form.content.data, author= current_user)
        db.session.add(post)
        db.session.commit()
        flash('The post was created successfully', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', form= form, legend= 'New Post', title= 'Create Post')

# create a route that displays a single post
@posts.route('/post/<int:post_id>')
def post(post_id):
    post= Post.query.get_or_404(post_id)
    return render_template('post.html', title= post.title, post= post)

#Create post update route
@posts.route('/post/<int:post_id>/update', methods= ['GET', 'POST'])
@login_required
def update_post(post_id):
    post= Post.query.get_or_404(post_id)
    if current_user!= post.author:
        abort(403)
    form= UserCreatePostForm()
    if form.validate_on_submit():
        post.title= form.title.data
        post.content= form.content.data
        db.session.commit()
        flash('You have successfully updated the post!', 'success')
        return redirect(url_for('posts.post', post_id= post.id))
    elif request.method== 'GET':
        form.title.data= post.title
        form.content.data= post.content
    return render_template('create_post.html', legend= 'Update Post', title= 'Update post', form= form)

# create a post delete route
@posts.route('/post/<int:post_id>/delete', methods= ['POST'])
@login_required
def delete_post(post_id):
    post= Post.query.get_or_404(post_id)
    if current_user!= post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('your post was successfully deleted!', 'success')
    return redirect(url_for('main.home'))
