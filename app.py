import os
import re
import json
import logging
import filetype
from cs50 import SQL
from PIL import Image
from datetime import datetime
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, flash, redirect, render_template, request, session
from helpers import apology, login_required, jsonify, has_picture, common_color

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["jsonify"] = jsonify
app.jinja_env.filters["has_picture"] = has_picture
app.jinja_env.filters["common_color"] = common_color

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# https://github.com/camptocamp/pytest-odoo/issues/15
logging.getLogger('PIL').setLevel(logging.INFO)


@app.errorhandler(404)
def page_not_found(e):
    return apology("Page not found", 404)


@app.route("/")
@login_required
def home():
    posts = db.execute("SELECT users.username, posts.*, json_array_length(likes) AS likes_count FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.id DESC")

    return render_template("home.html", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id, but maintain flashed message if present
    # https://www.reddit.com/r/cs50/comments/fw50k5/message_flashing_not_working_with_redirect_to/
    if session.get("_flashes"):
        flashes = session.get("_flashes")
        session.clear()
        session["_flashes"] = flashes
    else:
        session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT id, username, hash FROM users WHERE username = ?", request.form.get("username").strip())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]

        flash("Successfully logged in!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Successfully logged out!")
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")

        elif not re.match(r'^(?=^[^_]+_?[^_]+$)(?!^\d+$)\w{3,20}$', username):
            return apology("inappropriate username")

        elif not password:
            return apology("must provide password")

        elif not confirmation:
            return apology("must confirm password")

        elif re.search(r'\s', password):
            return apology("passwords cannot contain spaces")

        elif len(password) < 8 or len(password) > 20:
            return apology("passwords length must be between 8 and 20")

        elif password != confirmation:
            return apology("passwords don't match")

        try:
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, generate_password_hash(password))
        except ValueError:
            return apology("username already exists")

        flash("Registered! You can now login!")
        return redirect("/login")


@app.route("/search")
def search():
    if not (q := request.args.get("q").strip()):
        return redirect("/")

    users = db.execute("SELECT id, username, about, has_picture FROM users WHERE username LIKE ?", "%" + q.strip() + "%")
    posts = db.execute("SELECT users.username, posts.*, json_array_length(likes) AS likes_count, strftime('%m/%d at %I:%M%p', datetime) AS date FROM posts JOIN users ON posts.user_id = users.id WHERE content LIKE ? ORDER BY posts.id DESC", "%" + q.strip() + "%")

    return render_template("search.html", users=users, posts=posts)


@app.route("/profile")
def profile():
    if not (id := request.args.get("id")):
        return redirect("/")

    user = db.execute("SELECT id, username, about, friends, requests, sent, has_picture, has_cover FROM users WHERE id = ?", id)

    if not user:
        return apology("User not found", 404)

    posts = db.execute("SELECT users.username, posts.*, json_array_length(likes) AS likes_count, strftime('%m/%d at %I:%M%p', datetime) AS date FROM posts JOIN users ON posts.user_id = users.id WHERE posts.user_id = ? ORDER BY posts.id DESC", id)

    return render_template("profile.html", user=user[0], posts=posts)


@app.route("/friends")
@login_required
def friends():
    user = db.execute("SELECT friends, requests, sent FROM users WHERE id = ?", session["user_id"])

    friends_ids = json.loads(user[0]["friends"])
    requests_ids = json.loads(user[0]["requests"])
    sent_ids = json.loads(user[0]["sent"])

    query = "SELECT id, username, about, has_picture FROM users WHERE id IN ({})"

    # https://python-forum.io/thread-19588-post-85359.html#pid85359
    friends = db.execute(query.format(", ".join(["?" for _ in friends_ids])), *friends_ids) if friends_ids else []
    requests = db.execute(query.format(", ".join(["?" for _ in requests_ids])), *requests_ids) if requests_ids else []
    sent = db.execute(query.format(", ".join(["?" for _ in sent_ids])), *sent_ids) if sent_ids else []

    return render_template("friends.html", friends=friends, requests=requests, sent=sent)


@app.route("/settings")
@login_required
def settings():
    user = db.execute("SELECT id, about, has_picture, has_cover FROM users WHERE id = ?", session["user_id"])

    return render_template("settings.html", user=user[0])


@app.route("/settings_profile", methods=["POST"])
@login_required
def settings_profile():
    about = request.form.get("about").strip()
    has_picture = db.execute("SELECT has_picture FROM users WHERE id = ?", session["user_id"])[0]["has_picture"]
    has_cover = db.execute("SELECT has_cover FROM users WHERE id = ?", session["user_id"])[0]["has_cover"]

    if 'profilePicture' in request.files:
        profilePicture = request.files['profilePicture']
        if profilePicture.filename != '' and '.' in profilePicture.filename and filetype.is_image(profilePicture):
            has_picture = True
            im = Image.open(profilePicture)
            im.save(f'./static/images/profile/picture/{session["user_id"]}.png', 'PNG')
            postId =  db.execute("INSERT INTO posts (user_id, content, datetime, has_image) VALUES (?, ?, ?, ?)", session["user_id"], "Updated profile picture", datetime.now(), True)
            im.save(f'./static/images/posts/{postId}.png', 'PNG')

    if 'profileCover' in request.files:
        profileCover = request.files['profileCover']
        if profileCover.filename != '' and '.' in profileCover.filename and filetype.is_image(profileCover):
            has_cover = True
            im = Image.open(profileCover)
            im.save(f'./static/images/profile/cover/{session["user_id"]}.png', 'PNG')
            postId =  db.execute("INSERT INTO posts (user_id, content, datetime, has_image) VALUES (?, ?, ?, ?)", session["user_id"], "Updated profile cover", datetime.now(), True)
            im.save(f'./static/images/posts/{postId}.png', 'PNG')

    db.execute("UPDATE users SET about = ?, has_picture = ?, has_cover = ? WHERE id = ?", about, has_picture, has_cover, session["user_id"])

    flash("Saved successfully!")
    return redirect("/settings")


@app.route("/settings_remove/<type>", methods=["POST"])
@login_required
def settings_remove_image(type):
    if type not in ["picture", "cover"]: return

    if os.path.exists(os.path.join(f"./static/images/profile/{type}/", f"{session["user_id"]}.png")):
        os.remove(f"./static/images/profile/{type}/{session["user_id"]}.png")

    db.execute(f"UPDATE users SET has_{type} = FALSE WHERE id = ?", session["user_id"])

    flash(f"Removed {type} image successfully")
    return redirect("/settings")


@app.route("/settings_password", methods=["POST"])
@login_required
def settings_password():
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if not current_password:
        return apology("must provide current password", 403)

    if not new_password:
        return apology("must provide new password", 403)

    elif not confirm_password:
        return apology("must confirm password", 403)

    elif re.search(r'\s', new_password):
        return apology("passwords cannot contain spaces", 403)

    elif len(new_password) < 8 or len(new_password) > 20:
        return apology("new password's length must be between 8 and 20", 403)

    elif new_password != confirm_password:
        return apology("passwords don't match", 403)

    hash = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])[0]["hash"]

    if not check_password_hash(hash, current_password):
        return apology("current password is invalid", 403)

    elif check_password_hash(hash, new_password):
        return apology("this is already the current password", 403)

    db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_password), session["user_id"])

    flash("Updated password! Please relogin!")
    return redirect("/login")


@app.route("/post", methods=["POST"])
@login_required
def post():
    content = request.form.get("content").strip()
    has_image = False

    if 'postImage' in request.files:
        postImage = request.files['postImage']

        if postImage.filename != '' and '.' in postImage.filename and filetype.is_image(postImage):
            has_image = True

    if not content and not has_image:
        return apology("Please include text and/or image to post")

    postId =  db.execute("INSERT INTO posts (user_id, content, datetime, has_image) VALUES (?, ?, ?, ?)", session["user_id"], content, datetime.now(), True if has_image else False)

    if has_image:
        im = Image.open(postImage)
        im.save(f'./static/images/posts/{postId}.png', 'PNG')

    flash("Posted successfully!")
    return redirect("/")


@app.route("/repost", methods=["POST"])
@login_required
def repost():
    post_id = request.form.get("post_id")

    if not post_id:
        return apology("No post id")

    post = db.execute("SELECT content, has_image FROM posts WHERE posts.id = ?", post_id)

    if not post:
        return apology("Invalid post id")

    new_post_id =  db.execute("INSERT INTO posts (user_id, content, datetime, has_image) VALUES (?, ?, ?, ?)", session["user_id"], post[0]["content"], datetime.now(), True if post[0]["has_image"] else False)

    if post[0]["has_image"]:
        os.popen(f'cp ./static/images/posts/{post_id}.png ./static/images/posts/{new_post_id}.png')

    flash("Reposted successfully")
    return redirect("/")


@app.route("/delete_post", methods=["POST"])
@login_required
def delete_post():
    postId = request.form.get("post_id")

    if not postId:
        return apology("No post id")

    post = db.execute("SELECT user_id, has_image FROM posts WHERE id = ?", postId)

    if not post:
        return apology("Invalid post id")

    if post[0]["user_id"] != session["user_id"]:
        return apology("Not authorized", 401)

    db.execute("DELETE FROM posts WHERE id = ?", postId)

    if post[0]["has_image"]:
        os.remove(f'./static/images/posts/{postId}.png')

    flash("Deleted post successfully!")
    return redirect("/")


@app.route("/posts")
def posts():
    if not (id := request.args.get("id")):
        return redirect("/")

    post = db.execute("SELECT users.username, posts.*, json_array_length(likes) AS likes_count, strftime('%m/%d at %I:%M%p', datetime) AS date FROM posts JOIN users ON posts.user_id = users.id WHERE posts.id = ?", id)

    if not post:
        return apology("Post not found")

    return render_template("post_expand.html", post=post[0])


@app.route("/like", methods=["post"])
@login_required
def like():
    post_id = request.get_json().get('post_id')

    if not post_id:
        return apology("No post id was provided")

    post_likes = db.execute("SELECT likes FROM posts WHERE id = ?", post_id)

    if not post_likes:
        return apology("Invalid post id")

    likes_array = json.loads(post_likes[0]["likes"])

    if session["user_id"] in likes_array:
        likes_array.remove(session["user_id"])
    else:
        likes_array.append(session["user_id"])

    db.execute("UPDATE posts SET likes = json_array(?) WHERE id = ?", likes_array, post_id)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route("/friend_request", methods=["post"])
@login_required
def friend_request():
    user_id = request.get_json().get("user_id")

    if not user_id:
        return apology("No user id was provided")

    user = db.execute("SELECT friends, requests, sent FROM users WHERE id = ?", user_id)

    if not user:
        return apology("Invalid user id")

    user_friends = json.loads(user[0]["friends"])
    user_requests = json.loads(user[0]["requests"])
    user_sent = json.loads(user[0]["sent"])

    if session["user_id"] in user_friends:
        return apology("Already friends")

    if session["user_id"] in user_requests:
        return apology("Already sent")

    if session["user_id"] in user_sent:
        # Make them friends
        # https://stackoverflow.com/a/15480983
        return redirect('/accept_friend', code=307)

    db.execute("UPDATE users SET requests = json_insert(requests, '$[#]', ?) WHERE id = ?", session["user_id"], user_id)
    db.execute("UPDATE users SET sent = json_insert(sent, '$[#]', ?) WHERE id = ?", user_id, session["user_id"])

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route("/cancel_request", methods=["post"])
@login_required
def cancel_request():
    user_id = request.get_json().get("user_id")

    if not user_id:
        return apology("No user id was provided")

    user = db.execute("SELECT requests FROM users WHERE id = ?", user_id)

    if not user:
        return apology("Invalid user id")

    user_requests = json.loads(user[0]["requests"])

    if session["user_id"] not in user_requests:
        return apology("Already canceled")

    sender = db.execute("SELECT sent FROM users WHERE id = ?", session["user_id"])
    sender_sent = json.loads(sender[0]["sent"])

    user_requests.remove(session["user_id"])
    sender_sent.remove(user_id)

    db.execute("UPDATE users SET requests = json_array(?) WHERE id = ?", user_requests, user_id)
    db.execute("UPDATE users SET sent = json_array(?) WHERE id = ?", sender_sent, session["user_id"])

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route("/remove_request", methods=["post"])
@login_required
def remove_request():
    user_id = request.get_json().get("user_id")

    if not user_id:
        return apology("No user id was provided")

    user = db.execute("SELECT sent FROM users WHERE id = ?", user_id)

    if not user:
        return apology("Invalid user id")

    user_sent = json.loads(user[0]["sent"])

    if session["user_id"] not in user_sent:
        return apology("You didn't receive a request from that user")

    receiver = db.execute("SELECT requests FROM users WHERE id = ?", session["user_id"])
    receiver_requests = json.loads(receiver[0]["requests"])

    user_sent.remove(session["user_id"])
    receiver_requests.remove(user_id)

    db.execute("UPDATE users SET requests = json_array(?) WHERE id = ?", receiver_requests, session["user_id"])
    db.execute("UPDATE users SET sent = json_array(?) WHERE id = ?", user_sent, user_id)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route("/accept_friend", methods=["post"])
@login_required
def accept_friend():
    user_id = request.get_json().get("user_id")

    if not user_id:
        return apology("No user id was provided")

    user = db.execute("SELECT sent, friends FROM users WHERE id = ?", user_id)

    if not user:
        return apology("Invalid user id")

    user_friends = json.loads(user[0]["friends"])

    if session["user_id"] in user_friends:
        return apology("Already friends")

    user_sent = json.loads(user[0]["sent"])

    if session["user_id"] not in user_sent:
        return apology("They didn't send you a request")

    accepter_requests = json.loads(db.execute("SELECT requests FROM users WHERE id = ?", session["user_id"])[0]["requests"])

    user_sent.remove(session["user_id"])
    accepter_requests.remove(user_id)

    db.execute("UPDATE users SET sent = json_array(?), friends = json_insert(friends, '$[#]', ?) WHERE id = ?", user_sent, session["user_id"], user_id)
    db.execute("UPDATE users SET requests = json_array(?), friends = json_insert(friends, '$[#]', ?) WHERE id = ?", accepter_requests, user_id, session["user_id"])

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route("/unfriend", methods=["post"])
@login_required
def unfriend():
    user_id = request.get_json().get("user_id")

    if not user_id:
        return apology("No user id was provided")

    user = db.execute("SELECT friends FROM users WHERE id = ?", user_id)

    if not user:
        return apology("Invalid user id")

    user_friends = json.loads(user[0]["friends"])

    if session["user_id"] not in user_friends:
        return apology("Not friends")

    canceler = db.execute("SELECT friends FROM users WHERE id = ?", session["user_id"])
    canceler_friends = json.loads(canceler[0]["friends"])

    user_friends.remove(session["user_id"])
    canceler_friends.remove(user_id)

    db.execute("UPDATE users SET friends = json_array(?) WHERE id = ?", user_friends, user_id)
    db.execute("UPDATE users SET friends = json_array(?) WHERE id = ?", canceler_friends, session["user_id"])

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route("/recover")
def recover():
    return apology("Try to remember it")

