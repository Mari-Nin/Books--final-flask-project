from datetime import datetime
from src.ext import db
from src.models.base import BaseModel

class Book(BaseModel):
    __tablename__= "books"
    id= db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String())
    title = db.Column(db.String())
    quantity = db.Column(db.Integer())
    status=db.Column(db.String())
    category = db.Column(db.String())
    img = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_completed = db.Column(db.String(), default="Completed")
    action_time = db.Column(db.DateTime,default = datetime.now)
    exchange_with = db.Column(db.String(255), nullable=True)
    


