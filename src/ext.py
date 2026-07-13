
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin,AdminIndexView,expose

# from src.admin_views.base import SecureIndexView

db=SQLAlchemy()
migrate=Migrate()  
login_manager = LoginManager()


class HomeAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False

admin = Admin(name = "BookMarket",index_view=HomeAdminIndexView())

jwt = JWTManager()