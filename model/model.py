from typing import Set

from sqlalchemy import Column, Integer, String
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
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    question = Column(String, nullable=False)
