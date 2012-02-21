from base import Database
from user.User import UserBase

def build_order():
    return 10

def build():
    engine = Database.create_sqlalchemy_engine()
    UserBase.metadata.create_all(engine)
