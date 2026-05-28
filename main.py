from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Column, JSON
from datetime import datetime
from decimal import Decimal

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    login_id: str
    login_password: str
    name: str
    is_admin: bool | None = Field(default=False)

class Contest(SQLModel, table=True):
    __tablename__ = "contests"
    id: int | None = Field(default=None, primary_key=True)
    title: str
    start_at: str
    end_at: str
    problem_ids: list[int] = Field(default=[], sa_column=Column(JSON))

class Problem(SQLModel, table=True):
    __tablename__ = "problems"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    time_limit: float
    memory_limit: int
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


SUPABASE_URL = "postgresql+psycopg://postgres.htzaogsomyseeipswygh:zPFnsDDZ2ShH@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"
engine = create_engine(SUPABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#ユーザー
@app.post("/users/")
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/")
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

#コンテスト
@app.put("/contests/{contest_id}")
def update_contest(contest_id: int, updated_contest: Contest, session: SessionDep) -> Contest:
    contest = session.get(Contest, contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="Contest not found")

    contest.problem_ids = updated_contest.problem_ids

    contest.title = updated_contest.title
    contest.start_at = updated_contest.start_at
    contest.end_at = updated_contest.end_at

    session.add(contest)
    session.commit()
    session.refresh(contest)
    return contest

@app.post("/contests/")
def create_contest(contest: Contest, session: SessionDep) -> Contest:
    session.add(contest)
    session.commit()
    session.refresh(contest)
    return contest

@app.get("/contests/")
def read_contests(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Contest]:
    contests = session.exec(select(Contest).offset(offset).limit(limit)).all()
    return contests

@app.get("/contests/{contest_id}")
def read_contest(contest_id: int, session: SessionDep) -> Contest:
    contest = session.get(Contest, contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="Contest not found")
    return contest

@app.delete("/contests/{contest_id}")
def delete_contest(contest_id: int, session: SessionDep):
    contest = session.get(Contest, contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="Contest not found")
    session.delete(contest)
    session.commit()
    return {"ok": True}

#問題problems
@app.put("/problems/{problem_id}")
def update_problem(problem_id: int, updated_problem: Problem, session: SessionDep) -> Problem:
    problem = session.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    problem.name = updated_problem.name
    problem.time_limit = updated_problem.time_limit
    problem.memory_limit = updated_problem.memory_limit

    session.add(problem)
    session.commit()
    session.refresh(problem)
    return problem

@app.post("/problems/")
def create_problem(problem: Problem, session: SessionDep) -> Problem:
    session.add(problem)
    session.commit()
    session.refresh(problem)
    return problem

@app.get("/problems/")
def read_problems(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Problem]:
    problems = session.exec(select(Problem).offset(offset).limit(limit)).all()
    return problems

@app.get("/problems/{problem_id}")
def read_problem(problem_id: int, session: SessionDep) -> Problem:
    problem = session.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@app.delete("/problems/{problem_id}")
def delete_problem(problem_id: int, session: SessionDep):
    problem = session.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    session.delete(problem)
    session.commit()
    return {"ok": True}
