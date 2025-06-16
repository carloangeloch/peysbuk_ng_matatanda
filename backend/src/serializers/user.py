from pydantic import BaseModel, ConfigDict

class PostUserSerializer(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    middle_name: str
    last_name:str
    avatar_url: str


class LoginUserSerializer(BaseModel):
    email: str
    password: str

class GetUserSerializer(BaseModel):
    username: str
    email: str
    first_name: str
    middle_name: str
    last_name:str

    model_config = ConfigDict(from_attributes=True)