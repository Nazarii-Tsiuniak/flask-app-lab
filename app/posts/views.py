from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.posts import post_bp
from app.posts.models import Post, Tag
from app.posts.forms import PostForm
from app import db
from flask_login import current_user

# --- Список постів ---
@post_bp.route('/')
def list_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template('posts/posts.html', posts=posts)

# --- Створення поста ---
@post_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author_id=form.author_id.data,
            is_active=form.enabled.data,
            posted=form.publish_date.data
        )
        # додаємо вибрані теги
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        post.tags = selected_tags

        db.session.add(post)
        db.session.commit()
        flash("Пост створено!", "success")
        return redirect(url_for('post_bp.list_posts'))

    return render_template('posts/add_post.html', form=form, edit=False)

# --- Деталі поста ---
@post_bp.route('/<int:id>')
def post_detail(id):
    post = Post.query.get_or_404(id)
    return render_template('posts/detail_post.html', post=post)

# --- Редагування поста ---
@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash("Ви не можете редагувати цей пост", "warning")
        return redirect(url_for('post_bp.list_posts'))

    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data

        post.tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()

        db.session.commit()
        flash("Пост оновлено!", "success")
        return redirect(url_for('post_bp.post_detail', id=post.id))

    return render_template('posts/add_post.html', form=form, edit=True)

# --- Видалення поста ---
@post_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash("Ви не можете видаляти цей пост", "warning")
        return redirect(url_for('post_bp.list_posts'))

    db.session.delete(post)
    db.session.commit()
    flash("Пост видалено!", "success")
    return redirect(url_for('post_bp.list_posts'))
