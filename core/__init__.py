from flask import Flask
from core.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth


db = SQLAlchemy()
migrate = Migrate()
marshmallow = Marshmallow()
jwt = JWTManager()
bcrypt = Bcrypt()
oauth = OAuth()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    oauth.init_app(app)

    with app.app_context():

        from core.todos.routes import tasks_blueprint
        from core.users.routes import users_blueprint

        # from core.social_auth.google.routes import google_blueprint
        # from core.social_auth.twitter.routes import twitter_blueprint
        # from core.social_auth.github.routes import github_blueprint

        app.register_blueprint(tasks_blueprint)
        app.register_blueprint(users_blueprint)
        # app.register_blueprint(google_blueprint)
        # app.register_blueprint(twitter_blueprint)
        # app.register_blueprint(github_blueprint)

        return app
