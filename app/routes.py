import os , secrets
from app import app, db, bcrypt, mail, Message, mail_username
from flask import render_template, url_for, flash, request, redirect
from flask_login import current_user, login_user , logout_user
from app.forms import msgForm, SignUpForm, ImageForm, SignInForm, PostForm
from app.models import user, blogpost
from datetime import datetime


@app.route("/", methods=["GET", "POST"])
def home_page():
    n = 5
    all_post = blogpost.query.order_by(blogpost.date.desc()).filter_by(publish=True)
    if request.method == "POST":
        n += 5
        return render_template("index.html", all_post=all_post, n=n)
    if request.method == "GET":
        return render_template("index.html", all_post=all_post, n=n)

@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/contact', methods=["GET", "POST"])
def contact_page():
    form = msgForm()

    if request.method == "POST":
        if form.validate_on_submit():
            msg = Message(subject=f"A message from {form.name.data}",
                          recipients=["hrittika23.st05@gmail.com"], 
                          body=f"Name: {form.name.data}!\n Email: {form.email.data}\n Phone Number: {form.phone.data}\n\n Message: {form.message.data}. \n\n\n Thank You!",
                          sender=mail_username)
            mail.send(msg)
            flash("Thanks for your message!", category="success")
            return redirect(url_for("contact_page"))
        else:
            return render_template("contact.html", form=form)


    if request.method == "GET":
        return render_template("contact.html", form=form)

@app.route('/post/<post_id>')
def post_page(post_id):
    post = blogpost.query.filter_by(id=post_id).first()
    return render_template("post.html", post=post)

@app.route('/add-post', methods=["GET", "POST"])
def add_post_page():
    form=PostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            blog_info = blogpost(title=form.title.data,
                                 subtitle=form.subtitle.data,
                                 body=form.body.data,
                                 author=f"@{current_user.username}",
                                 date=datetime.now(),
                                 post_owner=current_user.id)
            img_info = form.post_bg.data
            if img_info:
                img_name=save_image(img_info)
                blog_info.post_pic = img_name
                db.session.commit()
            if "save" in request.form:
                db.session.add(blog_info)
                db.session.commit()
            if "publish" in request.form:
                blog_info.publish = True
                db.session.add(blog_info)
                db.session.commit()
            return redirect(url_for("home_page"))
    return render_template("add_post.html", form=form)

@app.route('/edit-post/<post_id>', methods=["GET", "POST"])
def edit_post_page(post_id):
    form=PostForm()
    post=blogpost.query.filter_by(id=post_id).first()

    if request.method == "POST":
        if post.title != form.title.data:
            post.title = form.title.data
            db.session.commit()
        if post.subtitle != form.subtitle.data:
            post.subtitle = form.subtitle.data
            db.session.commit()
        if post.body != form.body.data:
            post.body = form.body.data
            db.session.commit()
        
        return redirect(url_for('my_post_page'))

    return render_template("edit_post.html", post=post, form=form)

@app.route('/my-posts', methods=["GET", "POST"])
def my_post_page():
    my_posts = blogpost.query.filter_by(post_owner=current_user.id)
    if request.method == "POST":
        if "delete_post" in request.form:
            if request.form.get("delete_post"):
                post_to_delete=blogpost.query.filter_by(id=request.form.get("delete_post")).first_or_404()
                db.session.delete(post_to_delete)
                db.session.commit()

        if "publish_post" in request.form:
            if request.form.get("publish_post"):
                post_to_publish=blogpost.query.filter_by(id=request.form.get("publish_post")).first_or_404()
                post_to_publish.publish = True
                db.session.commit()

        return redirect(url_for("my_post_page"))
    return render_template("my_post.html", my_posts=my_posts)

def save_image(img_info):
    random_hex = secrets.token_hex(8)
    _ , ext = os.path.splitext(img_info.filename)
    img_name = random_hex + ext
    save_path = os.path.join(app.root_path,'static/profile_up',img_name)

    img_info.save(save_path)

    return img_name
@app.route('/image-upload', methods=["GET", "POST"])
def image_upload():
    form=ImageForm()
    if request.method == "POST":
        if form.validate_on_submit():
            img_name = save_image(form.img.data)
            current_user.image = img_name
            db.session.commit()
            return redirect(url_for("home_page"))
        else:
            return render_template("image.html", form=form)
    return render_template("image.html", form=form)

@app.route('/sign-up', methods=["GET", "POST"])
def sign_up_page():
    form=SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user_info = user(username=form.username.data,
                             email=form.email.data,
                             f_name=form.name.data,
                             password=hashed_password)
            db.session.add(user_info)
            db.session.commit()
            login_user(user_info)

            flash(f"Created an account for {form.username.data}", category="success")
            return redirect(url_for("image_upload"))
        else:
            return render_template("sign_up.html", form=form)
    return render_template("sign_up.html", form=form)

@app.route('/sign-in', methods=["GET", "POST"])
def sign_in_page():
    form = SignInForm()
    if request.method == "POST":
        if form.validate_on_submit():
            attempted_user = user.query.filter_by(username=form.username.data, email=form.email.data).first()
            if attempted_user:
                password_check = bcrypt.check_password_hash(attempted_user.password, form.password.data)
                if password_check:
                    login_user(attempted_user)
                    flash(f"Successfully signed in as {attempted_user.username}", category="success")
                    return redirect(url_for('home_page'))
                else:
                    flash("Password doesn't match!", category="danger")
            else:
                flash("username/email is not registered!", category="danger")

    return render_template("sign_in.html", form=form)

@app.route('/sign-out')
def sign_out_page():
    logout_user()
    flash("Signed Out!", category="success")
    return redirect(url_for('home_page'))