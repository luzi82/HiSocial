from sqlalchemy import Column, String
from base.DatabaseBase import DBB

GROUP_ID_LENGTH = 8

class Group(DBB):
    
    __tablename__ = "hs_user_group"

    group_id = Column(String(GROUP_ID_LENGTH), primary_key=True)
    name = Column(String(32),nullable=False)

    def __init__(self, group_id, name):
        self.group_id = group_id
        self.name = name

def add(session,group_id, name):
    '''
    Add user
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type group_id: str
    :param group_id: The group id
    
    :type name: str
    :param name: The group name
    '''
    new_group = Group(group_id=group_id,name=name)
    session.add(new_group)
    session.flush()

def delete(session,group_id):
    '''
    Delete group
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type group_id: str
    :param group_id: The group id
    
    :rtype: boolean
    :return: True iff success
    '''
    ret = session.query(Group).filter(Group.group_id==group_id).delete() > 0
    session.flush()
    return ret

def rename(session,group_id, name):
    '''
    Rename group
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type group_id: str
    :param group_id: The group id
    
    :type name: str
    :param name: The new group name

    :rtype: boolean
    :return: True iff success
    '''
    ret = session.query(Group).filter(Group.group_id==group_id).update({Group.name:name}) > 0
    session.flush()
    return ret

def get_name(session,group_id):
    '''
    Get group name
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type group_id: str
    :param group_id: The group id
    
    :rtype: str
    :return: group name, None if not exist
    '''
    t = session.query(Group.name).filter(Group.group_id==group_id).first()
    if t == None : return None
    if len(t) < 1 : return None
    return t[0]
