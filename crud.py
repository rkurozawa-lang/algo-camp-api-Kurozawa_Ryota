from sqlalchemy.orm import Session
from . import models, schemas

def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()
