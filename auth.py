from flask import Blueprint, request,jsonify, render_template,redirect, url_for, flash
from flask_login import login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from models import Authors
auth = Blueprint('auth', __name__)


def check_email(email):
    try:
        validate = validate_email(email)
        email = validate.email
        print(email)
        return email
    except EmailNotValidError as e:
        flash("The email address is invalid")

@auth.route("/signin", methods=['GET','POST'])
def signin():
    if request.method=='GET':
        return render_template("pages/login.html")
    else:
        email =check_email(request.form.get("email"))
        password = request.form.get("password")

        author = Authors.query.filter(Authors.email == email).one_or_none()
        print(author)
        if not author or not check_password_hash(author.password,password):
            flash("Wrong User credentials, please check and try again")
            return redirect("auth.signin")
        else:
            login_user(author)
            return redirect(url_for("main.blog"))



@auth.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("pages/signup.html")
    else:
        email=request.form.get('email');
        username=request.form.get("username");
        password=request.form.get('password');
        confirm_password=request.form.get("confirm_password");
        check_email(email)

        if password != confirm_password:
            flash("Password Not Matching")
            return redirect(url_for("auth.signup"))

        if len(confirm_password) < 8 and len(password) < 8:
            flash("Password must be atleast 8 characters")
            return redirect(url_for("auth.signup"))
            
        else:
            pwd = generate_password_hash(password, "sha256")
            new_author = Authors(password=pwd,email=email, username=username)
            new_author.insert()

    return redirect(url_for("auth.signin"))


@auth.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for("main.index"))