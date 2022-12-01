from .models.models import User
from .routes.auth import auth
from .routes.views import views
from flask import Flask, jsonify, render_template
from werkzeug import exceptions
# from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_cors import CORS
from .database.db import db

DB_NAME = 'database.db'

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = "helloworld"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)


app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")


with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"message": f"Oops... {err}"}), 404


@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({"message": f"It's not you it's us"}), 500


if __name__ == "__main__":
    app.run(debug=True)
