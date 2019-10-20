import hashlib
from models.auth import User, Post
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


def register(username, password):
    """
    用户注册数据交互操作
    :param username:
    :param password:
    :return:
    """
    s = Session()
    s.add(User(name=username, password=hashed(password)))
    s.commit()
    s.close()


def add_post(image_url, thumb_url, username):
    """
    上传图片保存到数据库
    :param image_url:
    :param username:
    :return:
    """
    session = Session()
    user = session.query(User).filter_by(name=username).first()
    post = Post(image_url=image_url, thumb_url=thumb_url, user=user)
    session.add(post)
    session.commit()
    post_id = post.id
    session.close()
    return post_id


def get_all_posts():
    session = Session()
    posts = session.query(Post).all()
    return posts


def get_post(post_id):
    session = Session()
    post = session.query(Post).filter_by(id=post_id).first()
    return post