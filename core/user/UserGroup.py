from sqlalchemy import Column, String
from sqlalchemy.schema import ForeignKey
from user import User
import Group
from base.DatabaseBase import DBB

class UserGroup(DBB):
    
    __tablename__ = "hs_user_usergroup"
    
    user_id = Column(String(User.USER_ID_LENGTH),ForeignKey("hs_user_user.user_id"), primary_key=True)
    group_id = Column(String(Group.GROUP_ID_LENGTH),ForeignKey("hs_user_group.group_id"), primary_key=True)
#    user_relationsip = relationship("User", backref="parent_assocs")
#    group_relationsip = relationship("Group", backref="parent_assocs")
     
    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id

def join(session,user_id,group_id):
    '''
    Add user to group
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type group_id: str
    :param group_id: The group id

    :type user_id: str
    :param user_id: The user id
    '''
    session.add(UserGroup(user_id=user_id,group_id=group_id))
    session.flush()

def unjoin(session,user_id,group_id):
    '''
    Remove user from group
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type group_id: str
    :param group_id: The group id

    :type user_id: str
    :param user_id: The user id

    :rtype: boolean
    :return: True iff success
    '''
    ret = session.query(UserGroup).filter(UserGroup.user_id==user_id).filter(UserGroup.group_id==group_id).delete() > 0
    session.flush()
    return ret

def get_group(session,user_id):
    '''
    Get user group
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type group_id: str
    :param group_id: The group id

    :type user_id: str
    :param user_id: The user id

    :rtype: boolean
    :return: True iff success
    '''
    t = session.query(UserGroup.group_id).filter(UserGroup.user_id==user_id).all()
    if t == None : return []
    return [ i[0] for i in t ]
