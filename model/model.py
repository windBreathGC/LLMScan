from enum import IntEnum
from typing import Set, Dict

from sqlalchemy import Column, Integer, String, Text, BigInteger, SmallInteger, DateTime, Boolean, Index
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


class Status(IntEnum):
    INIT = 0
    EXECUTING = 1
    FINISHED = 2
    EXCEPTION = 3
    SUCCESS = 4
    FAILED = 5


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def get_fields(cls) -> Set:
        return cls._meta.fields - cls._meta.fetch_fields

    @classmethod
    def get_fields_map(cls) -> Dict:
        return cls._meta.field_map


class PromptModel(BaseModel):
    """测试用例"""
    __tablename__ = "t_prompt"
    id = Column(Integer, primary_key=True, doc="主键", autoincrement=True)
    prompt_id = Column(String(36), unique=True, nullable=False, doc="用于关联其它表，唯一")
    type = Column(String(36), nullable=False, doc="类型")
    level = Column(Integer, default=Level.LOW, doc="级别")
    prompt = Column(String(512), nullable=False, doc="提示词内容")
    response = Column(String(1024), nullable=True, doc="参考回答")
    is_public = Column(Boolean, nullable=True, doc="公共用例")
    # 联合索引
    __table_args__ = (Index('ix_type_level_is_public', 'type', 'level', 'is_public'),)


class RecordModel(BaseModel):
    """测试记录"""
    __tablename__ = "t_record"
    id = Column(Integer, primary_key=True, doc="主键", autoincrement=True)
    record_id = Column(String(36), unique=True, nullable=False, doc="用于关联其它表，唯一")
    type = Column(String(512), nullable=False, doc="类型")
    level = Column(Integer, default=Level.LOW, doc="级别")
    prompt = Column(String(512), nullable=False, doc="提示词内容")
    response = Column(Text(), nullable=True, doc="大模型应答内容")
    score = Column(Integer, default=0, doc="评测得分")
    user_id = Column(String(36), nullable=True, doc="用户id")
    create_time = Column(DateTime, nullable=True, doc="创建时间")
    update_time = Column(DateTime, nullable=True, doc="更新时间")
    # 联合索引
    __table_args__ = (Index('ix_type_level_user_id_create_time', 'type', 'level', 'user_id', 'create_time'),)


class TaskModel(BaseModel):
    """任务"""
    __tablename__ = "t_task"
    id = Column(Integer, primary_key=True, doc="主键", autoincrement=True)
    task_id = Column(String(36), unique=True, nullable=False, doc="用于关联其它表，唯一")
    name = Column(String(255), nullable=False, doc="任务名")
    status = Column(Integer, default=Status.INIT, doc="当前状态")
    progress = Column(Integer, default=0, doc="执行进度")
    user_id = Column(String(36), nullable=True, doc="用户id")
    create_time = Column(DateTime, nullable=True, doc="创建时间")
    update_time = Column(DateTime, nullable=True, doc="更新时间")
    finish_time = Column(DateTime, nullable=True, doc="完成时间")
    # 联合索引
    __table_args__ = (Index('ix_status_user_id_create_time_finish_time', 'status', 'user_id',
                            'create_time', 'finish_time'),)
