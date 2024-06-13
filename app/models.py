from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    role: str  # User role: doctor, nurse, patient
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Message(BaseModel):
    sender_id: str
    receiver_id: str
    content: str
