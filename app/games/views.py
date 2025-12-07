# app/games/views.py
import os
from flask import (
    render_template, request, redirect, url_for, flash, current_app, abort
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from PIL import Image

from app import db
from . import games_bp
from .models import Game, Genre
from .forms import GameForm, DeleteGameForm

# helper to save image and create thumb 128x128
def save_image(file_storage, folder="game_images"):
    filename = secure_filename(file_storage.filename)
    upload_folder = os.path.join(current_app.root_path, "static", folder)
    os.makedirs(upload_folder, exist_ok=True)
    full_path = os.path.join(upload_folder, filename)
    file_storage.save(full_path)

    # create thumbnail 128x128, prefix thumb_
    try:
        img = Image.open(full_path)
        img.thumbnail((128, 128))
        thumb_name = f"thumb_{filename}"
        thumb_path = os.path.join(upload_folder, thumb_name)
        img.save(thumb_path)
    except Exception:
        thumb_name = None

    return filename, (thumb_name or None)


# LIST + SEARCH
@games_bp.route("/", methods=["GET"])
def list_games():
    q = request.args.get("q", "").strip()
    sort = request.args.get("sort", "title")
    page = request.args.get("page", 1, type=int)

    query = Game.query
    if q:
        query = query.filter(Game.title.ilike(f"%{q}%"))

    # safe sort
    if sort == "price":
        query = query.order_by(Game.price.asc())
    elif sort == "created":
        query = query.order_by(Game.created_at.desc())
    else:
        query = query.order_by(Game.title.asc())

    games = query.paginate(page=page, per_page=10, error_out=False)

    # встановлюємо фото
    for game in games.items:
        if not game.image_filename:
            default_path = f"{game.id}.jpg"
            full_path = os.path.join(current_app.root_path, "static", "game_images", default_path)
            if os.path.exists(full_path):
                game.image_filename = default_path
            else:
                game.image_filename = "default_game.jpg"

    return render_template("games/list_games.html", games=games, q=q, sort=sort)


# DETAIL
@games_bp.route("/<int:game_id>")
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    
    if not game.image_filename:
        default_path = f"{game.id}.jpg"
        full_path = os.path.join(current_app.root_path, "static", "game_images", default_path)
        if os.path.exists(full_path):
            game.image_filename = default_path
        else:
            game.image_filename = "default_game.jpg"

    # форма для видалення
    delete_form = DeleteGameForm()

    return render_template("games/detail_game.html", game=game, delete_form=delete_form)


# CREATE
@games_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_game():
    form = GameForm()
    form.set_genre_choices()

    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename, thumb = save_image(form.image.data)

        new_game = Game(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data or 0.0,
            genre_id=form.genre.data,
            owner_id=current_user.id,
            image_filename=filename,
            created_at=datetime.utcnow()
        )
        db.session.add(new_game)
        db.session.commit()
        flash("Гру створено", "success")
        return redirect(url_for("games.game_detail", game_id=new_game.id))

    return render_template("games/create_edit_game.html", form=form, action="create")


# EDIT
@games_bp.route("/<int:game_id>/edit", methods=["GET", "POST"])
@login_required
def edit_game(game_id):
    game = Game.query.get_or_404(game_id)
    if game.owner_id != current_user.id:
        abort(403)

    form = GameForm()
    form.set_genre_choices()

    if request.method == "GET":
        form.title.data = game.title
        form.description.data = game.description
        form.price.data = game.price
        form.genre.data = game.genre_id

    if form.validate_on_submit():
        game.title = form.title.data
        game.description = form.description.data
        game.price = form.price.data or 0.0
        game.genre_id = form.genre.data

        if form.image.data:
            filename, thumb = save_image(form.image.data)
            game.image_filename = filename

        db.session.commit()
        flash("Гру оновлено", "success")
        return redirect(url_for("games.game_detail", game_id=game.id))

    return render_template("games/create_edit_game.html", form=form, action="edit", game=game)


# DELETE
@games_bp.route("/<int:game_id>/delete", methods=["POST"])
@login_required
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    if game.owner_id != current_user.id:
        abort(403)

    db.session.delete(game)
    db.session.commit()
    flash("Гру видалено", "info")
    return redirect(url_for("games.list_games"))
