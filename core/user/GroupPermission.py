from base.DatabaseBase import DBB
from sqlalchemy import Column, String, func, Integer, Boolean
from sqlalchemy.schema import ForeignKey
import Group
import sqlalchemy.orm.exc
from base.Runtime import trace

GROUP_PERMISSION_NAME_LENGTH = 128
KEY_ORDER = "order"
KEY_ENABLE = "enable"

class GroupPermission(DBB):
    
    __tablename__ = "hs_user_grouppermission"

    group_id = Column(String(Group.GROUP_ID_LENGTH),ForeignKey("hs_user_group.group_id"), primary_key=True)
    permission_name = Column(String(GROUP_PERMISSION_NAME_LENGTH), primary_key=True)
    order = Column(Integer,nullable=False)
    enable = Column(Boolean,nullable=False)

    def __init__(self, group_id, permission_id,order,enable):
        self.group_id = group_id
        self.permission_name = permission_id
        self.order = order
        self.enable = enable
    
    def __repr__(self):
        return "<GroupPermission(%s,%s,%d,%d)>" %\
            (self.group_id, self.permission_name, self.order,self.enable)

def set(session,group_id,permission_id,order,enable):
    '''
    Set permission
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type group_id: str
    :param group_id: The group id
    
    :type permission_name: str
    :param permission_name: The permission id
    
    :type order: int
    :param order: The permission order
    
    :type enable: boolean
    :param enalbe: permit
    '''
    q = session.\
        query(GroupPermission).\
        filter(GroupPermission.group_id==group_id).\
        filter(GroupPermission.permission_name==permission_id)
    i = q.count()
    if i == 0 :
        gp = GroupPermission(group_id,permission_id,order,enable)
        session.add(gp)
        session.flush()
    elif i == 1 :
        q.update({GroupPermission.order:order,GroupPermission.enable:enable})
        session.flush()
    else :
        raise AssertionError()

def unset(session,group_id,permission_name):
    '''
    Set permission
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type group_id: str
    :param group_id: The group id
    
    :type permission_name: str
    :param permission_name: The permission id
    '''
    session.query(GroupPermission).filter(GroupPermission.group_id==group_id).filter(GroupPermission.permission_name==permission_name).delete()
    session.flush()

def get(session,group_id,permission_name):
    '''
    Get permission
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type group_id: str
    :param group_id: The group id
    
    :type permission_name: str
    :param permission_name: The permission id
    
    :rtype: map
    :return: [KEY_ORDER]=key order, [KEY_ENABLE]=enable
    '''
    try:
        v = session.\
            query(GroupPermission.order,GroupPermission.enable).\
            filter(GroupPermission.group_id==group_id).\
            filter(GroupPermission.permission_name==permission_name).\
            one()
    except sqlalchemy.orm.exc.NoResultFound:
        return None
    except sqlalchemy.orm.exc.MultipleResultsFound:
        raise AssertionError()
    ret = {KEY_ORDER:v[0],KEY_ENABLE:v[1]}
    return ret
