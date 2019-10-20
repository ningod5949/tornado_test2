from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime)

from models.db import Base


# 创建用户表模型
class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50))
    create_time = Column(DateTime, default=datetime.now)


if __name__ == '__main__':
    Base.metadata.create_all()      # 创建表



