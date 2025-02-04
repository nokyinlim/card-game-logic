"""
This file should contain some database helper functions and schemas (namely for table accounts) for the database. 
Other utils such as SessionDep, get_session() and engine are stored here, although some other files still use their own
"""

import json
from typing import Annotated, Optional

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel, Session

from defaults import default_user_stats



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


class AccountBase(SQLModel):
    username: str = Field(unique=True, index=True)
    hashed_password: str
    stats: str = json.dumps(default_user_stats)

class Account(AccountBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class AccountCreate(AccountBase):
    pass

class AccountRead(AccountBase):
    id: int

class AccountUpdate(AccountBase):
    pass

