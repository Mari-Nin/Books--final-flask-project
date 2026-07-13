
from flask import Flask
from flask_admin.menu import MenuLink
from src.config import Config
from flask import url_for
from src.ext import db, migrate,login_manager,admin,jwt

from src.models.book import Book
from src.models.user import User

from src.views.main.routes import main_bp
from src.views.auth.routes import auth_bp
from src.views.book.routes import book_bp

from src.commands import init_db, populate_db 

from src.admin_views.user import UserView
from src.admin_views.book import Bookview



blueprints = [main_bp, auth_bp, book_bp]
commands = [init_db, populate_db] 

blueprints=[main_bp,auth_bp,book_bp]
commands = [init_db, populate_db]

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

   
    register_blueprint(app)
    register_extentions(app)
    register_commands(app)
  
    
    return app

def register_extentions(app):
    db.init_app(app)
    migrate.init_app(app,db)

    login_manager.init_app(app)
    login_manager.login_view = 'main.index'


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    jwt.init_app(app)

    @jwt.user_lookup_loader
    def user_lookup_loader(jwt_header, jwt_data):
        user_id = jwt_data['sub']
        return User.query.get(user_id)
        



    admin.init_app(app)
    admin.add_view(UserView(User, db.session))
    admin.add_view(Bookview(Book, db.session))    

    admin.add_link(MenuLink('Logout', url='/logout'))
    admin.add_link(MenuLink('Site', url='/'))

def register_blueprint(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

def register_commands(app):
    for command in commands:
        app.cli.add_command(command)
   


    