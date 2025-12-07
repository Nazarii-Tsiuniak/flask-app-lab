# app/games/__init__.py
from flask import Blueprint

games_bp = Blueprint("games", __name__, template_folder="templates", static_folder="../static")

