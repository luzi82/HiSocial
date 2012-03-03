from user.GroupPermission import GroupPermission
from user.UserGroup import UserGroup
from sqlalchemy.sql.expression import desc

def get_user_permission(session,user_id,permission_name):
    '''
    Get permission of a user
    
    :type session: sqlalchemy.orm.session.Session
    :param session: sqlalchemy DB Session
    
    :type user_id: str
    :param user_id: The user id
    
    :type permission_name: str
    :param permission_name: The permission id
    
    :rtype: boolean
    :return: permission enabled
    '''
    q=session.\
        query(GroupPermission.enable).\
        filter(UserGroup.user_id==user_id).\
        filter(GroupPermission.permission_name==permission_name).\
        filter(GroupPermission.group_id==UserGroup.group_id).\
        order_by(desc(GroupPermission.order)).\
        first()
    if q == None : return False
    return q[0]
