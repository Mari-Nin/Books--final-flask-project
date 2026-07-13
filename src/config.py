from os import path

class Config:
    SECRET_KEY = "asd1d2g3d;IOISie0w09"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(path.dirname(__file__),"test.db")

    UPLOAD_PATH = path.join(path.dirname(__file__), 'static', 'uploads')