from base.DatabaseBase import DBB
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, BINARY
import binascii
import time

class XBT_FILES(DBB):

    __tablename__ = 'xbt_files'

    #fid int not null auto_increment,
    #    primary key (fid),
    fid = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    #info_hash binary(20) not null,
    #    unique key (info_hash)
    info_hash = Column(BINARY(20), nullable=False, unique=True, key="info_hash")
    #leechers int not null default 0,
    leechers = Column(INTEGER, nullable=False, server_default="0")
    #seeders int not null default 0,
    seeders = Column(INTEGER, nullable=False, server_default="0")
    #completed int not null default 0,
    completed = Column(INTEGER, nullable=False, server_default="0")
    #flags int not null default 0,
    flags = Column(INTEGER, nullable=False, server_default="0")
    #mtime int not null,
    mtime = Column(INTEGER, nullable=False)
    #ctime int not null,
    ctime = Column(INTEGER, nullable=False)

    def __init__(self, info_hash, mtime, ctime):
        self.info_hash = info_hash
        self.mtime = mtime
        self.ctime = ctime

    def __repr__(self):
        return "<XBT_FILES(%d,%s,%d,%d,%d,%d,%d,%d)>" % \
            (self.fid, binascii.b2a_hex(self.info_hash), self.leechers, self.seeders, self.completed, self.flags, self.mtime, self.ctime)

def add_hash(session, hash_hex):
    hash_bin = binascii.a2b_hex(hash_hex)
    c = session.query(XBT_FILES).filter(XBT_FILES.info_hash == hash_bin).count()
    if(c > 0):
        return
    
    timestamp = __timestamp()
    session.add(XBT_FILES(info_hash=hash_bin, mtime=timestamp, ctime=timestamp))
    session.flush()

def __timestamp():
    return int(time.time())
