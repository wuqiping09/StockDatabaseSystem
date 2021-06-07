from .models import User,Admin

def uniqueId(u_id, identity):
    '''
    检查在所属identity下userid是否已经存在
    :param u_id: 需要检查id
           identity: 用户所属分类
    :return: bool
    '''
    if identity == 'User':
        user = User.query.filter(User.user_id == u_id).first()
        if user:
            return False
        else:
            return True
    else:
        admin = Admin.query.filter(Admin.admin_id == u_id).first()
        if admin:
            return False
        else:
            return True

def hasChinese(s):
    """
    检查整个字符串是否包含中文
    :param s: 需要检查的字符串
    :return: bool
    """
    for ch in s:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def hasSpace(s):
    """
    检查整个字符串是否包含空格
    :param s: 需要检查的字符串
    :return: bool
    """
    if ' ' in s:
        return True
    return False
