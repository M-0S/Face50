import json
import filetype
from cs50 import SQL
import fast_colorthief
from os.path import exists
from functools import wraps
from flask import redirect, render_template, session

db = SQL("sqlite:///database.db")

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def jsonify(text):
    if not text:
        return ""

    return json.loads(text)


def has_picture(user_id):
    if not user_id:
        return False

    user = db.execute("SELECT has_picture FROM users WHERE id = ?", user_id)

    if not user:
        return False

    return user[0]["has_picture"]


def common_color(image_path):
    if not image_path:
        return (0, 0, 0)

    if not exists(image_path):
        return (0, 0, 0)

    if not filetype.is_image(image_path):
        return (0, 0, 0)

    return fast_colorthief.get_dominant_color(image_path, quality=1)

