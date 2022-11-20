from flask import Flask, request
from models import setup_db, Authors
from flask_login import LoginManager
from flask_moment import Moment
moment = Moment()
def create_app():
    app =Flask(__name__)

    # moment = Moment(app)
    moment.init_app(app)

    setup_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.signin"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(authors_id):
        return Authors.query.get(authors_id)


    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
# app = create_app(prod_config)