from flask import Flask
from core.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth
from celery import Celery
from flask_mail import Mail
from flask.logging import default_handler
from logging.config import dictConfig

dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
            'custom_formatter': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers':
            {
                'debug_handler': {
                    'class': 'logging.FileHandler',
                    'formatter': 'custom_formatter',
                    'filename': 'logs/debug.log',
                    'level': 'DEBUG',
                },
                'info_handler': {
                    'class': 'logging.FileHandler',
                    'formatter': 'custom_formatter',
                    'filename': 'logs/info.log',
                    'level': 'INFO',
                },
                'warning_handler': {
                    'class': 'logging.FileHandler',
                    'formatter': 'custom_formatter',
                    'filename': 'logs/warnings.log',
                    'level': 'WARN',
                },
                'error_handler': {
                    'class': 'logging.FileHandler',
                    'formatter': 'custom_formatter',
                    'filename': 'logs/errors.log',
                    'level': 'ERROR',
                }
            },
        'root': {
            'handlers': ['debug_handler', 'info_handler', 'warning_handler', 'error_handler']
        },
    })

db = SQLAlchemy()
migrate = Migrate()
marshmallow = Marshmallow()
jwt = JWTManager()
bcrypt = Bcrypt()
oauth = OAuth()
mail = Mail()

""" Instantiate Celery, celery uses lowercase in loading the config variables,
    while flask only considers uppercase variables as config,
    so manually pass broker and result_backend
"""
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, result_backend=Config.RESULT_BACKEND)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    oauth.init_app(app)
    mail.init_app(app)
    celery.conf.update(app.config)

    app.logger.removeHandler(default_handler)

    with app.app_context():
        from core.todos.routes import tasks_blueprint
        from core.users.routes import users_blueprint

        from core.users.social_auth_routes import social_auth_blueprint

        app.register_blueprint(tasks_blueprint)
        app.register_blueprint(users_blueprint)
        app.register_blueprint(social_auth_blueprint)

        return app
