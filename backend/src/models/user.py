from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str
    first_name: str
    middle_name: str= Field(default=None, nullable=True)
    last_name:str
    avatar_url: str = Field(default=None, nullable=True)