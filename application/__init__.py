from flask import Flask
from os import path
import os
from os.path import join, dirname
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager

# Get the values from the .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

db = SQLAlchemy()

# The function below will be responsible for
# creating the Flask web application and
# setting up the SQLite database
def createApp():
    # app is the Flask web application
    app = Flask(__name__)
    # Here we set the  Database URI for the application
    app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('SQLALCHEMY_DATABASE_URI')
    db.init_app(app)
    # Create the database if it is not already there
    from .models import User, InventoryItem
    if path.exists('application/' + os.environ.get('DATA_BASE_NAME')) == False:
        db.create_all(app=app)
    # register the routes
    from .routes import routes
    from .auth import auth
    app.register_blueprint(routes, url_prefix="/")
    app.register_blueprint(auth, url_prefix='/')
    # The secret key must be set for the app as well
    app.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

    