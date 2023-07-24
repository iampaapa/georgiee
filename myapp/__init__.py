import os

from flask import Flask 

from .extensions import db
from .routes import main

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    # postgres://georgette_project_user:xOLCvgOroVw5S4C3BBFbdTdasca4Qts6@dpg-ciuio7liuiedpv0b2prg-a.oregon-postgres.render.com/georgette_project

    db.init_app(app)

    app.register_blueprint(main)

    return app