from base import Database
from user.User import UserBase
from user.Group import GroupBase

def build_order():
    return 10

def build():
    engine = Database.create_sqlalchemy_engine()
    UserBase.metadata.create_all(engine)
    GroupBase.metadata.create_all(engine)
