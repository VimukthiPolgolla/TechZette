from flask import Flask
from firebase import firebase
from os import path


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
