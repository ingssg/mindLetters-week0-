from flask import Blueprint, render_template

articles_blueprint = Blueprint("articles_blueprint", __name__, template_folder="../templates/articles")


@articles_blueprint.route("/")
def get_all_articles():
    return render_template('index.html')
