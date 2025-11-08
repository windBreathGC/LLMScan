from typing import Set

from sqlalchemy import Column, Integer, String, SmallInteger, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = None

    @classmethod
    def get_fields(cls) -> Set:
        return cls._meta.fields - cls._meta.fetch_fields


class Prompt(BaseModel):
    """测试用例"""
    __tablename__ = "t_prompt"
    id = Column(Integer, primary_key=True, doc="主键")
    prompt_id = Column(String, length=36, unique=True, nullable=False, doc="用于关联其它表，唯一")
    type = Column(String, nullable=False, doc="类型")
    level = Column(SmallInteger, default=1, doc="级别")
    prompt = Column(String, length=512, nullable=False, doc="提示词内容")
    response = Column(String, length=1024, nullable=True, doc="参考回答")


class Record(BaseModel):
    """测试记录"""
    __tablename__ = "t_record"
    id = Column(Integer, primary_key=True, doc="主键")
    record_id = Column(String, length=36, unique=True, nullable=False, doc="用于关联其它表，唯一")
    type = Column(String, nullable=False, doc="类型")
    level = Column(SmallInteger, default=1, doc="级别")
    prompt = Column(String, length=512, nullable=False, doc="提示词内容")
    response = Column(Text, nullable=True, doc="大模型应答内容")
    score = Column(SmallInteger, default=1, doc="评测得分")
