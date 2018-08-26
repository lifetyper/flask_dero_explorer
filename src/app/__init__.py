# coding=utf-8
import os
import logging
from flask import Flask
from flask_bootstrap import Bootstrap


app_name = 'dero_explorer'

bootstrap = Bootstrap()
basedir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(basedir, os.pardir))
main_dir = os.path.join(basedir, 'main')
static_dir = os.path.join(root_dir, 'static')


def create_app():
    app = Flask(app_name)
    bootstrap.init_app(app)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config['SECRET_KEY'] = 'hioSfaep4if43DF89342ri'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    logging.basicConfig(level=logging.INFO)

    return app
