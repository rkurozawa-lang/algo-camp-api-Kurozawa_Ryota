from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base() # type: ignore

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # ....supabase上のusersテーブルとカラム数や種類をあわせる
    questions = relationship("Question", back_populates="author")

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_active = Column(Integer)
    created_at = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    # ....supabase上のusersテーブルとカラム数をあわせる
    author = relationship("User", back_populates="questions")