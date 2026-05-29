from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
class UserBase(BaseModel):
    id: int
    name: str
# ここにはmodelsと同じだけのカラムを定義しても構わないし、足りなくても構わない。

    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    id: int
    title: str
    is_active: bool
    created_at: datetime
# ここにはmodelsと同じだけのカラムを定義しても構わないし、足りなくても構わない。
class Config:
    orm_mode = True

class UserWithQuestions(UserBase):
    questions: List[QuestionBase] = []

class QuestionWithAuthor(QuestionBase):
    author: UserBase