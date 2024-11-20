<div align="center" style="text-align: center">
<h1>Face50</h1>
<p>Video Demo: https://youtu.be/-28KNUeXx5Y</p>
<img src="https://i.imgur.com/6rFQxaY.png" alt="Face50" width=720>

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
</div>

# Description
A social media site like FaceBook but with my own personal touch! I created this website without taking any courses other than CS50x, however, I had to do a lot of Google and Stackoverflow searching. I didn't use any AI tools to create this project or its documentation though.
# Support
If you want to help me through my learning journey and help me get a better PC, then you can via [PayPal](https://www.paypal.com/paypalme/gerodev).
# Features
- Responsive design to support all screens.
- Registration page with these rules:
    - Usernames must be 3 to 20 characters long.
    - Passwords must be 8 to 20 characters long.
    - Usernames can only contain letters, numbers, and _.
    - Usernames can have at most one _, but not start nor end with it.
    - Usernames cannot be all numbers.
- Fancy and mobile-friendly navigation bar.
- Themes dropdown to switch between light, dark, and auto modes.
- Toast messages with an animated progress bar.
- Posting function where posts can contain text and/or images.
- Posts contain their creation date in the format of "just now", "a minute ago", etc...
- Post uses the most common color of the image (if it has one) as a background for that image. Also uses lightbox to display images.
- Ability to like, unlike, repost, share, copy, expand, and delete posts.
- Hashtags feature where hashtags are colored in blue and clicking them shows all posts that contain that hashtag.
- Search function to search through users and posts.
- Home page that lists all recent posts made by users ordered by post date.
- Profile page for each user that lists their posts and allows them to customize their profile picture, cover and about.
- Friending function allows you to send, cancel, remove, and accept friend requests, then you can unfriend users.
- Friends page where you can view and manage your friends, requests you received, and requests you have sent.
- Settings page to customize your profile and update your password.
- Handled many bad use cases and errors, and implemented some security practices from week 10.
- And a lot more...
# Code Explaination
## `.py` files
### `app.py`
#### Intro
Atop the file are a bunch of imports, they will be explained when used.

First `flask.Flask` is configured, then `Jinja` is configured with some custom filters that are defined in `helpers.py` and will be explained later. Next, `Flask` is configured to store `sessions` on the local filesystem instead of cookies. The file then configures `cs50`’s `SQL` module to use `database.db`, more on it below. Next, the `logging` level is set to `INFO` to make sure information about `DEBUG` is not logged and shown in the terminal. Next is an error handler for code `404`. Notice how `apology` function (defined in `helpers.py`) is used here.

#### Database
`database.db` has two tables: `users` and `posts`.<br/>
`users` table contains nine columns:
- `id` with type `INTEGER`. This is the primary key. It will auto-increment by default.
- `username` with type `TEXT`. `COLLATE NOCASE` is used on this column to make it case-insensitive. Also a `UNIQUE INDEX` is created on this column to prevent duplicates.
- `hash` with type `TEXT`.
- `about` with type `TEXT`.
- `has_picture` with type `BOOLEAN`.
- `has_cover` with type `BOOLEAN`.
- `friends` with type `TEXT`, default is an empty array (`[]`). This will store an array of friends' ids of user.
- `requests` with type `TEXT`, default is an empty array (`[]`).
- `sent` with type `TEXT`, default is an empty array (`[]`).

`posts` table contains six columns:
- `id` with type `INTEGER`. This is the primary key. It will auto-increment by default.
- `user_id` with type `INTEGER`.
- `content` with type `TEXT`.
- `datetime` with type `TEXT`.
- `has_image` with type `BOOLEAN`.
- `likes` with type `TEXT`, default is `[]`.

#### `/` <sup>GET</sup>
When requested, `db.execute` is used to query `database.db` to get all posts from `posts` table ordered descendingly by `id` to make sure newest posts are shown first. Notice how `json_array_length` function is used in the query to get number of likes of each post. Finally, using `flask`'s `render_template` function, [`home.html`](#homehtml) template is rendered with the variable `posts`.<br/>
Notice how this route and some other routes are decorated with `@login_required` (a function defined in `helpers.py`). That decorator ensures that, if a user tries to visit any of those routes, he or she will first be redirected to `login` so as to log in.

#### `/login` <sup>GET, POST</sup>
First, some lines of code are typed to make sure `flashes` are saved (if any) before clearing `session`. When this route is requested via `GET`, [`login.html`](#loginhtml) template is rendered.<br/>
When it is requested via `POST`, it first handles some cases. Next, it uses `db.execute` to query `database.db`. Next, it uses `werkzeug.security`'s `check_password_hash` to compare hashes of users’ passwords. After that, login remembers that a user is logged in by storing his or her `user_id` and `user_name`, in `session`. That way, any of this file’s routes can check which user, if any, is logged in. Finally, notice how once the user has successfully logged in, a success message is flashed via `flask`'s `flash` function, then using `flask`'s `redirect` function, `login` will redirect to [`"/"`](#-get), taking the user to their home page.

#### `/logout` <sup>GET</sup>
`logout` simply clears `session`, effectively logging a user out. Next, a flash message is made, then the user is redirected to [`/login`](#login-get-post).

#### `/register` <sup>GET, POST</sup>
When requested via `GET`, [`register.html`](#registerhtml) template is rendered.<br/>
When requested via `POST`, some `if` statements are used to validate `username`, `password`, and `confirmation`. Notice how `match` and `search` functions from `re` are used here to make use of [regex](https://en.wikipedia.org/wiki/Regular_expression). Next, a query is made on `database.db` to store new user's data in `users` table. Notice how `generate_password_hash` function from `werkzeug.security` module is used here to generate a [hash](https://en.wikipedia.org/wiki/Cryptographic_hash_function) for the user's password. Finally, a flash message is made and the user is redirected to [`/login`](#login-get-post).

#### `/search` <sup>GET</sup>
A database query is made on both `users` and `posts` tables to get all results relevant to the search. Notice how `strftime` function is used in the query to format `datetime`. At last [`search.html`](#searchhtml) template is rendered with these results.

#### `/profile` <sup>GET</sup>
A database query is made to get user's data using `id`. After that, another database query is made to get all of that user's posts. Finally, [`profile.html`](#profilehtml) template is rendered with these data.

#### `/friends` <sup>GET</sup>
A database query is made to get all of user's friends, requests user received, and requests user made. Next, `loads` function from `json` library is used to convert the query's resulting arrays (stored as `string`s in the database) to a standard Python `list` (aka array). Next, multiple database queries are made to get data about each user in the `friends_ids`, `requests_ids`, and `sent_ids` lists. Finally, [`friends.html`](#friendshtml) template is rendered with all of these data.

#### `/settings` <sup>GET</sup>
In short, these values: `id`, `about`, `has_picture`, and `has_cover` are queried from `users` table to be used in [`settings.html`](#settingshtml) template that is rendered after.

#### `/settings_profile` <sup>POST</sup>
This route is used to update user's profile. When requested, we first get user's `about` from `form`. `about` will be always sent in the `form` whether user changes it or not. Next, we make a database query to check for `has_picture` and `has_cover` values of the user. This step is to make sure if these values were `True`, then they should be kept `True` in the final database query.<br/>
Next, we check if the user wanted to update his or her profile picture by checking whether `request.files` had `profilePicture` in or not. If so, we need to make some validations first to check if it is a valid image or not. Notice how `is_image` function from `filetype` library is used here. If it is a valid image, we change `has_picture` value to `True`, then we use `PIL.Image` module to `open` and `save` new user's picture. After that, a new post is made to announce that the user has updated his or her profile picture. Notice how `now` function from `datetime.datetime` module is used to get the current date and time to be used in the database query. Next, all these steps are made again for user's cover. Notice how all images for posts, profiles' pictures, and profiles' cover images are saved in `PNG` format. Finally, a database query is made to store new values, then a flash message is made and user is redirected to [`/settings`](#settings-get).

#### `/settings_remove/<type>` <sup>POST</sup>
This route is used to remove user's profile picture or cover. Notice how this route has a path parameter `<type>` in its URL. This `<type>` can only be `picture` or `cover`. Notice how `path.exists` and `path.join` functions from `os` library are used here to check whether the user has `type` image or not. If so, then `remove` function from `os` library is used to remove that image. Finally, a database query is made to set `has_{type}` of that user to `FALSE`, then a flash message is made and user is redirected to [`/settings`](#settings-get).

#### `/settings_password` <sup>POST</sup>
This route is used to update user's password. When requested, we first validate `current_password`, `new_password`, and `confirm_password`. Next, we make a database query to update user's password, then a flash message is made and user is redirected to [`/login`](#login-get-post) to log in again.

#### `/post` <sup>POST</sup>
This route is used to make posts. Posts must contain text and/or image to be posted. When requested, we get post `content` (if any) from `form`, then we check if the post has an image. If the post doesn't have content or image, then it won't be posted, else we will make a database query on `posts` table to save new post data, then we will use `Image` library to save post's image (if it has one), then a flash message is made and user is redirected to [`"/"`](#-get).

#### `/repost` <sup>POST</sup>
As obvious, this route is used to repost an existing post. When requested, we get the post that the user wants to repost by post's id, then we check if it is a valid post. After that, we insert new post's data into the `posts` database table and make a copy of the original post's image (if it has one) using `popen` function from `os` library. Finally, a flash message is made and the user is redirected to [`"/"`](#-get).

#### `/delete_post` <sup>POST</sup>
Used to delete a post by its `id`. We first make sure that it's a valid post `id` and that it belongs to this user. Then we delete the post from the database and delete its image (if any). Finally, a flash message is made and the user is redirected to [`"/"`](#-get).

#### `/posts` <sup>GET</sup>
Used to view a post by its `id` when `expand` button in the post's layout is clicked. Simply, we make sure it's a valid post `id` and if so, we render [`post_expand.html`](#post_expandhtml) template.

#### `/like` <sup>POST</sup>
Used to like or unlike a post. When requested, we first validate the post's `id`. Notice how `get_json` function of `flask.request` is used here. Reason for that is because `request` is not made this time via `form`, but via a JavaScript function called `fetch`. Next, we use `loads` function from `json` library as we did in the [`/friends`](#friends-get) route to convert `likes` array from `string` to a standard Python `list`. After that, we check whether the user is trying to like or unlike the post. Finally, we update the post's `likes` count, then we return a success message using `json`'s `dumps` function. Now this might be confusing, unlike previous routes, no template is rendered nor redirect is made, that's because `request` is made via `fetch` as we mentioned above. So we need to return an [HTTP status code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status). In this case, we are returning `200 OK`.

#### `/friend_request` <sup>POST</sup>
Used to make friend requests. We first get the id of the user that the friend request is being sent to. Next, we validate that id and query `users` table to get `friends`, `requests`, and `sent` arrays of that user. Next, we check that the friend request sender is not in `friends` or `sent` arrays. If the receiver had sent a request to the sender before, then we redirect the sender to [`/accept_friend`](#accept_friend-post) route with code `307` to preserve the request type as originally sent (read [here](https://stackoverflow.com/a/15480983) for more info). After that, we make a database query to update `requests` array for receiver, and `sent` array for sender, using SQLite's [`json_insert`](https://www.sqlite.org/json1.html#jins) function. Finally, we return status code `200 OK`.

#### `/cancel_request` <sup>POST</sup>
Used by users to cancel friend requests they have sent to others. We first get the receiver's data and check if he or she has received a friend request from this user. If so, we remove the sender's id from the receiver's `requests` array, and remove the receiver's id from the sender's `sent` id. Finally, we return status code `200 OK`.

#### `/remove_request` <sup>POST</sup>
Used by users to remove friend requests they have received from others. We first get the sender's data and check if he or she has sent a friend request to this user. If so, we remove the sender's id from the receiver's `requests` array, and remove the receiver's id from the sender's `sent` id. Finally, we return status code `200 OK`.

#### `/accept_friend` <sup>POST</sup>
Used by users to accept friend requests they have received from others. We first get the sender's data and check that his or her `friends` array doesn't contain the accepter's id. Then we check that sender's `sent` array contains the accepter's id. If so, we update `sent` and `friends` arrays for the sender. Then we update `requests` and `friends` arrays for the accepter. Finally, we return status code `200 OK`.

#### `/unfriend` <sup>POST</sup>
When requested, we make sure both users are friends. If so, we update `friends` array for both users. Finally, we return status code `200 OK`.

#### `/recover` <sup>GET</sup>
Try to remember it! :P
<br><br>

### `helpers.py`
#### Intro
This file is from CS50's week 9 problem set, [Finance](https://cs50.harvard.edu/x/2024/psets/9/finance/). I've modified it in this project.

#### `apology`
Explaination from CS50's [website](https://cs50.harvard.edu/x/2024/psets/9/finance/#helperspy):<br/>
> Next take a look at `helpers.py`. Ah, there’s the implementation of `apology`. Notice how it ultimately renders a template, [`apology.html`](#apologyhtml). It also happens to define within itself another function, `escape`, that it simply uses to replace special characters in apologies. By defining `escape` inside of `apology`, we’ve scoped the former to the latter alone; no other functions will be able (or need) to call it.

#### `login_required`
From CS50's [website](https://cs50.harvard.edu/x/2024/psets/9/finance/#helperspy):<br/>
> Next in the file is `login_required`. No worries if this one’s a bit cryptic, but if you’ve ever wondered how a function can return another function, here’s an example!

#### `jsonify`
The next functions in this file have been implemented by me. All of them are made to be used as custom filters in Jinja templates. The first one is `jsonify`, used to convert a string to JSON format (e.g. an array of users' ids). Jinja already has a custom filter called `tojson` but for some reason, it didn't work as expected so I had to make my own workaround.

#### `has_picture`
Used to check if a user has a profile picture or not. Returns `True` or `False`.

#### `common_color`
Used to get the most common color of an image using its path. `get_dominant_color` function from `fast_colorthief` library is used here. Returns the color as a tuple `(r, g, b)`.
<hr>

## `/static/js`
### `toggle_themes.js`
This file includes the function that makes themes switch work.

### `toast_message.js`
This file includes the function that makes Bootstap's [toast messages](https://getbootstrap.com/docs/5.3/components/toasts) work.

### `tooltips.js`
This file is used to initialize Bootstrap's [tooltips](https://getbootstrap.com/docs/5.3/components/tooltips).

### `validate_register.js`
This script is used by [`register.html`](#registerhtml) template as a client-sided verification for usernames and passwords. No worries if the user could bypass it as we have another layer of verification that is server-sided in [`/register`](#register-get-post) route.

### `modal_post.js`
Used by [`layout_post_modal.html`](#layoute_post_modalhtml) template to verify that the user has provided text and/or image to post before sending the data to the server.

### `modal_delete.js`
Used by [`layout_delete_modal.html`](#layout_delete_modalhtml) template to make it work and get the id of the post that the user wants to delete.

### `post_like.js`
Used to make posts' like button function. It updates the likes count for the local client by ±1 and changes the look of the thumbs up button. Next, it makes a `POST` request to [`/like`](#like-post) route using `fetch` method.

### `search.js`
Used by [`search.html`](#searchhtml) template to toggle switching between `users` and `posts` tabs in search.

### `friends_page.js`
Used by [`friends.html`](#friendshtml) template to toggle switching between `friends`, `requests`, and `sent` tabs.

### `friend_functions.js`
Used by [`friends.html`](#friendshtml) and [`profile.html`](#profilehtml) templates to make friending buttons (e.g. `Add Friend`, `Unfriend`, etc...) function.

### `settings_password.js`
Used by [`settings.html`](#settingshtml) template for the form that is used to update users' passwords.
<hr>

## `/static/css`
### `styles.css`
The stylesheet file for the project. Take a look at it to see which CSS properties and [custom Bootstrap properties](https://getbootstrap.com/docs/5.3/customize/css-variables/) (prefixed with `bs-`) were used.
<hr>

## `/static/images`
### `/icon`
Used to store website's `favicon.ico`.

### `/posts`
Used to store posts' images. Each post can have only 1 image. Each image is renamed to its post id and stored in `PNG` format.

### `/profile`
#### `/picture`
Used to store users' profile pictures. Each picture is renamed to its user id and stored in `PNG` format. This folder must contain an image named "_default.svg" that will be used as the default profile picture for new users.

#### `/cover`
Used to store users' profile cover images. Each cover is renamed to its user id and stored in `PNG` format.
<hr>

## `/templates`
### `apology.html`
From CS50's [website](https://cs50.harvard.edu/x/2024/psets/9/finance/#templates):<br/>
> In `apology.html`, meanwhile, is a template for an apology. Recall that `apology` in `helpers.py` took two arguments: `message`, which was passed to `render_template` as the value of `bottom`, and, optionally, `code`, which was passed to `render_template` as the value of `top`. Notice in `apology.html` how those values are ultimately used!

### `layout.html`
Notice how we used a JavaScript library called `moment` to format posts' dates. Also here you will find the elements that make the navbar. It also includes support for Flask’s [message flashing](https://flask.palletsprojects.com/en/1.1.x/quickstart/#message-flashing) so that you can relay messages from one route to another for the user to see. Notice how it defines a block, `main`, inside of which templates shall go. At the end of the file is a JavaScript library called `fslightbox` used to enable users to view posts' images, profiles' pictures, and profiles' cover images in fullscreen.

### `layout_users.html`
Here we make a Bootstrap [card](https://getbootstrap.com/docs/5.3/components/card) that shall list users. Used in [`search.html`](#searchhtml) and [`friends.html`](#friendshtml) templates.

### `layout_post_modal.html`
Here we create a Bootstrap [modal](https://getbootstrap.com/docs/5.3/components/modal) that will be used to enable users to create posts.

### `layout_delete_modal.html`
Here we create a Bootstrap [modal](https://getbootstrap.com/docs/5.3/components/modal) that will be used to enable users to delete posts.

### `layout_post.html`
The layout used for all posts to be displayed the same on different pages of the website. Here is the implementation of the hashtag, like, repost, and share functions besides the dropdown for each post that enables users to expand, copy, and delete posts.

### `post_expand.html`
Used to display each post on a separate page using the `expand` button.

### `login.html`
Here is the form used to login.

### `register.html`
Here is the form used to register.

### `home.html`
Used to display the home page for users.

### `search.html`
Used to display the search page for users.

### `profile.html`
Used to display the profile page for users.

### `friends.html`
Used to display the friends page for users.

### `settings.html`
Used to display the settings page for users. Notice how four forms are made at the top of the file to be used in different places in the page using `form` attribute on elements.
<hr>
