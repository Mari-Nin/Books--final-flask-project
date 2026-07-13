
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from src.models.base import BaseModel
from src.ext import db



class User(BaseModel,UserMixin):
    __tablename__="users" 
    
    id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    role = db.Column(db.String(24),default='user')
    _password = db.Column(db.String(128))


    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self,password):
        self._password = generate_password_hash(password)


    def is_admin(self):
        return self.role=='admin'
    
    def check_password(self, password):
        return check_password_hash(self._password, password)