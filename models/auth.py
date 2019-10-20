from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship

from models.db import Base


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

# 1个user对应多个post表
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='posts', uselist=False, cascade='all')     # backref反向指引，uselist不需要生成具体的列表
    # p.user.name
    # u.posts[0]    # 双向查询
    def __repr__(self):
        return "<User:#{}>".format(self.id)       # 格式化返回


if __name__ == '__main__':
    Base.metadata.create_all()      # 创建表



