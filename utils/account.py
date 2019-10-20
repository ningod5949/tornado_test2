import hashlib
from models.auth import User, Session
from models.db import Session


def hashed(text):
    """
    密码md5加密
    :param text: password
    :return:
    """
    return hashlib.md5(text.encode('utf8')).hexdigest()

def authenticate(username, password):
    """
    验证密码
    :param username:
    :param password:
    :return:
    """
    return User.get_password(username) == hashed(password)      # 返回bool值


# 用户注册数据交互操作
def register(username, password):
    s = Session()
    s.add(User(name=username, password=hashed(password)))
    s.commit()