from flask import Blueprint, render_template

users_blueprint = Blueprint("users_blueprint", __name__, template_folder="../templates/users")


@users_blueprint.route("/signin")
def signin():
    return render_template('signin.html')


@users_blueprint.route("/signup")
def signup():
    return render_template('signup.html')
