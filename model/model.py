from enum import IntEnum
from typing import Set, Dict

from sqlalchemy import Column, Integer, String, Text, BigInteger, SmallInteger, DateTime
from sqlalchemy.dialects.mysql import INTEGER as MYSQLINT, BIGINT
from sqlalchemy.orm import declarative_base

Base = declarative_base()
# 适用于mysql的自定义无符号整型
UnsignedInteger = Integer()
UnsignedInteger = UnsignedInteger.with_variant(MYSQLINT(unsigned=True), 'mysql')
UnsignedBigInteger = BigInteger()
UnsignedBigInteger = UnsignedBigInteger.with_variant(BIGINT(unsigned=True), 'mysql')


class Level(IntEnum):
    LOW = 1
    MIDDLE = 2
    HIGH = 3


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def get_fields(cls) -> Set:
        return cls._meta.fields - cls._meta.fetch_fields

    @classmethod
    def get_fields_map(cls) -> Dict:
        return cls._meta.field_map


class Prompt(BaseModel):
    """测试用例"""
    __tablename__ = "t_prompt"
    id = Column(Integer, primary_key=True, doc="主键", autoincrement=True)
    prompt_id = Column(String(36), unique=True, nullable=False, doc="用于关联其它表，唯一")
    type = Column(String(36), nullable=False, doc="类型")
    level = Column(Integer, default=Level.LOW, doc="级别")
    prompt = Column(String(512), nullable=False, doc="提示词内容")
    response = Column(String(1024), nullable=True, doc="参考回答")


class Datetime:
    pass


class Record(BaseModel):
    """测试记录"""
    __tablename__ = "t_record"
    id = Column(Integer, primary_key=True, doc="主键", autoincrement=True)
    record_id = Column(String(512), unique=True, nullable=False, doc="用于关联其它表，唯一")
    type = Column(String(512), nullable=False, doc="类型")
    level = Column(Integer, default=Level.LOW, doc="级别")
    prompt = Column(String(512), nullable=False, doc="提示词内容")
    response = Column(Text(), nullable=True, doc="大模型应答内容")
    score = Column(Integer, default=0, doc="评测得分")
    user_id = Column(String(36), nullable=True, doc="用户id")
    create_time = Column(DateTime, nullable=True, doc="用户id")
    update_time = Column(DateTime, nullable=True, doc="用户id")
