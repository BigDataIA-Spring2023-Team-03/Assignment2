from typing import List
from pydantic import BaseModel, EmailStr

# pydantic models are called schemas = response_models
class S3_Transfer(BaseModel):
    action: str
    src_bucket: str
    dest_bucket: str
    dest_folder: str
    prefix: str
    files_selected: str



class UserRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
