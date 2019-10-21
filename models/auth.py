from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists       # 查询存在

from models.db import Base, Session


session = Session()

# 创建用户表模型
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50))
    create_time = Column(DateTime, default=datetime.now)
    email = Column(String(80))

    def __repr__(self):
        return "<User:#{}-{}>".format(self.id, self.name)       # 格式化返回

    @classmethod
    def is_exists(cls, username):
        return session.query(exists().where(cls.name == username)).scalar()     # scalar返回查询对象的值

    @classmethod
    def get_password(cls, username):
        user = session.query(cls).filter_by(name=username).first()
        if user:
            return user.password
        else:
            return ''

# 1个user对应多个post表
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))
    thumb_url = Column(String(200))

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='posts', uselist=False, cascade='all')     # backref反向指引，uselist不需要生成具体的列表
    # p.user.name
    # u.posts[0]    # 双向查询
    def __repr__(self):
        return "<User:#{}>".format(self.id)       # 格式化返回


class Like(Base):
    """
    记录用户标记为喜欢的图片
    """
    __tablename__ = 'likes'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False, primary_key=True)



if __name__ == '__main__':
    Base.metadata.create_all()      # 创建表



