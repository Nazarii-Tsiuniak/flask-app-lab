from flask import render_template, redirect, url_for, flash, request, session
from app.posts import post_bp
from app import db
from app.posts.models import Post
from app.posts.forms import PostForm

# --- Список постів ---
@post_bp.route('/')
def list_posts():
    posts = Post.query.filter_by(is_active=True).order_by(Post.posted.desc()).all()
    return render_template('posts/posts.html', posts=posts)

# --- Створення поста ---
@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        author = session.get('user', 'Anonymous')
        post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data,
            category=form.category.data,
            is_active=form.enabled.data,
            author=author
        )
        db.session.add(post)
        db.session.commit()
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
        form.populate_obj(post)
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for('post_bp.post_detail', id=post.id))
    form.publish_date.data = post.posted
    return render_template('posts/add_post.html', form=form, edit=True)

# --- Видалення поста ---
@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "success")
        return redirect(url_for('post_bp.list_posts'))
    return render_template('posts/confirm_delete.html', post=post)
