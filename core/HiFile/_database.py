from base.DatabaseBase import DBB
from sqlalchemy import Column, String, func, Integer
from sqlalchemy.dialects.mysql import BINARY,INTEGER
from user import User
from sqlalchemy.schema import ForeignKey
import binascii

class Torrent(DBB):
    
    __tablename__ = "hs_hifile_torrent"
    
    torrent_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(String(User.USER_ID_LENGTH),ForeignKey("hs_user_user.user_id"))
    info_hash_bin = Column(BINARY(20), nullable=False)
    
    def __init__(self, user_id,info_hash_bin):
        self.user_id = user_id
        self.info_hash_bin = info_hash_bin

def add_torrent(session,user_id,info_hash_hex):
    info_hash_bin = binascii.a2b_hex(info_hash_hex)
    t=Torrent(user_id=user_id,info_hash_bin=info_hash_bin)
    session.add(t)
    session.flush()
    return t.torrent_id

def list_user_torrent(session,user_id):
    t = session.query(Torrent.torrent_id).filter(Torrent.user_id==user_id).all()
    if t == None : return []
    return [ i[0] for i in t ]
