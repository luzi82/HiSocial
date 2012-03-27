from base.DatabaseBase import DBB
from sqlalchemy import Column, String, func, Integer
from sqlalchemy.dialects.mysql import BINARY, INTEGER, BIGINT
from sqlalchemy.schema import ForeignKey
from user import User
import binascii

NAME_SIZE = 250

class Torrent(DBB):
    
    __tablename__ = "hs_hifile_torrent"
    
    torrent_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(String(User.USER_ID_LENGTH), ForeignKey("hs_user_user.user_id"))
    info_hash_bin = Column(BINARY(20), nullable=False)
    name = Column(String(NAME_SIZE), nullable=False)
    size = Column(BIGINT, nullable=False)
    
    def __init__(self, user_id, info_hash_bin, name, size):
        self.user_id = user_id
        self.info_hash_bin = info_hash_bin
        self.name = name
        self.size = size

def add_torrent(session, user_id, info_hash_hex, name, size):
    info_hash_bin = binascii.a2b_hex(info_hash_hex)
    t = Torrent(user_id=user_id, info_hash_bin=info_hash_bin, name=name, size=size)
    session.add(t)
    session.flush()
    return t.torrent_id

def list_user_torrent(session, user_id):
    t = session.query(Torrent.torrent_id).filter(Torrent.user_id == user_id).all()
    if t == None : return []
    return [ i[0] for i in t ]
