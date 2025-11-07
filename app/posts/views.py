from flask import render_template, redirect, url_for, flash, request, session
from app.posts import post_bp
from app.posts.models import Post
from app.posts.forms import PostForm

# --- Список постів ---
@post_bp.route('/')
def list_posts():
    posts = Post.active_posts().all()
    return render_template('posts/posts.html', posts=posts)

# --- Створення поста ---
@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        Post.create(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author=session.get('user', 'Anonymous'),
            is_active=form.enabled.data,
            posted=form.publish_date.data
        )
        flash("Post added successfully", "success")
        return redirect(url_for('post_bp.list_posts'))
    return render_template('posts/add_post.html', form=form, edit=False)

# --- Деталі поста ---
@post_bp.route('/<int:id>')
def post_detail(id):
    post = Post.query.get_or_404(id)
    return render_template('posts/detail_post.html', post=post)

# --- Редагування поста ---
@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.update(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.enabled.data,
            posted=form.publish_date.data
        )
        flash("Post updated successfully", "success")
        return redirect(url_for('post_bp.post_detail', id=post.id))
    form.publish_date.data = post.posted
    return render_template('posts/add_post.html', form=form, edit=True)

# --- Видалення поста ---
@post_bp.route('/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    post.delete()
    flash("Post deleted successfully", "success")
    return redirect(url_for('post_bp.list_posts'))
