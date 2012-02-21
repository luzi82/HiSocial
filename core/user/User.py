'''
@author: luzi82
'''

from base import Secret
from sqlalchemy import Column, String, func
from sqlalchemy.ext.declarative import declarative_base
import core_config
import string

PASSWORD_HASH_LENGTH = 53
USER_ID_LENGTH = 128

UserBase = declarative_base()
class User(UserBase):
    '''
    password hash are in SALT#base64(HASH) format
    '''
    
    __tablename__ = "user"

    user_id = Column(String(USER_ID_LENGTH), primary_key=True)
    password_hash = Column(String(PASSWORD_HASH_LENGTH))

    def __init__(self, user_id, password_hash):
        self.user_id = user_id
        self.password_hash = password_hash
        
    def __repr__(self):
        return "<User('%s','%s')>" % (self.user_id, self.password_hash)
    
def add_user_account(session, user_id, password):
    '''
    Add a user to database
    Does not check if user exist
    
    :type sess: sqlalchemy.orm.session.Session
    :param sess: sqlalchemy DB Session
    
    :type user_id: str
    :param user_id: The user_id
    
    :type passowrd: str
    :para, passowrd: The password
    
    :rtype: boolean
    :return: True iff success
    '''
    new_user = User(user_id=user_id, password_hash=_gen_password_hash(password))
    session.add(new_user)
    session.commit()


def check_user_account_exist(session, user_id):
    '''
    Check if a user exist
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type user_id: str
    :param user_id: The user_id to query
    
    :rtype: boolean
    :return: True iff user exist
    '''
    user_query = session.query(func.count(User.user_id)).filter(User.user_id == user_id).first()
    return user_query[0] > 0


def check_user_account_password(session, user_id, password):
    '''
    Check user password
    Return False if user not exist
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session

    :type user_id: str
    :param user_id: The user_id to query
    
    :type password: str
    :param password: The password to check
    
    :rtype: boolean
    :return: True iff user exist and match
    '''
    user_query = session.query(User.password_hash).filter(User.user_id == user_id).first()
    if(user_query == None): return False
    password_hash = user_query[0]
#    trace(password_hash)
    return _check_password_hash(password=password, hash_value=password_hash)

def check_user_id_valid(user_id):
    '''
    Check if user id can be used
    
    :type user_id: str
    '''
    if(user_id == None):return False
    if(len(user_id) < core_config.USER_ID_LENGTH_MIN):return False
    if(len(user_id) > core_config.USER_ID_LENGTH_MAX):return False
    if(user_id[0] not in string.ascii_letters):return False
    valid_char = string.ascii_letters + string.digits + "_-"
    for c in user_id:
        if (c not in valid_char) : return False
#    if(not user_id.isalnum()):return False
    return True

def check_password_valid(password):
    '''
    Check if user id can be used
    
    :type password: str
    '''
    if(password == None):return False
    if(len(password) < core_config.USER_ID_LENGTH_MIN):return False
    if(len(password) > core_config.USER_ID_LENGTH_MAX):return False
    valid_char = string.ascii_letters + string.digits + "_-"
    for c in password:
        if (c not in valid_char) : return False
    return True

def _gen_password_hash(password, salt=None):
    """
    Create salt+hash string from password
    Can be verified by _check_password_hash
    
    :type password: str
    :param password: The password to convert
    
    :type salt: str
    :param salt: Salt value.  If None, this func will generate by random
    
    :rtype: str
    :return: hash value in SALT#base64(HASH) format
    """
    return Secret.gen_hash(password, core_config.USER_ACCOUNT_PASSWORD_HMAC, salt)

def _check_password_hash(password, hash_value):
    """
    To check if the password match the hash
    
    :type hash_value: str
    :param hash_value: The hash value to check, in SALT#base64(HASH) format
    
    :type password: str
    :param password: The password to check
    
    :rtype: boolean
    :return: True iff match
    """
    return Secret.check_hash(password, core_config.USER_ACCOUNT_PASSWORD_HMAC, hash_value)
