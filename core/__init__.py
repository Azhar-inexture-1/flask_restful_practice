from flask import Flask
from core.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
marshmallow = Marshmallow()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():

        from core.todos.routes import tasks_blueprint
        from core.users.routes import users_blueprint

        app.register_blueprint(tasks_blueprint)
        app.register_blueprint(users_blueprint)

        return app
