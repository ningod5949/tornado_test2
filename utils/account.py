import hashlib
from models.auth import User, Post
from models.db import Session


db_session = Session()
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


class HandlerORM:
    """
    辅助操作数据库的工具类， 综合 RequestHandler使用
    """
    def __init__(self, db_session):
        """
        :param db_session: 由handler进行实例化和close
        """
        self.db_session = db_session

    def get_user(self, username):
        user = self.db_session.query(User).filter_by(name=username).first()
        return user

    def get_post(self, post_id):
        """
        返回特定的id 的post实例
        :param post_id:
        :return:
        """
        post = self.db_session.query(Post).filter_by(id=post_id).first()
        return post

    def register(self, username, password):
        """
        用户注册数据交互操作
        :param username:
        :param password:
        :return:
        """
        self.db_session.add(User(name=username, password=hashed(password)))
        self.db_session.commit()

    def add_post(self, image_url, thumb_url, username):
        """
        上传图片保存到数据库
        :param image_url:
        :param username:
        :return:
        """
        user = self.get_user(username)
        post = Post(image_url=image_url, thumb_url=thumb_url, user=user)
        self.db_session.add(post)
        self.db_session.commit()
        post_id = post.id
        return post_id

    def get_all_posts(self):
        posts = self.db_session.query(Post).all()
        return posts

    def get_posts_for(self, username):
        user = self.get_user(username)
        posts = self.db_session.query(Post).filter_by(user=user).all()
        return posts