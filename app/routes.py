from fastapi import APIRouter, HTTPException, Depends
from app.models import User, Token, Message
from app.dependencies import get_password_hash, verify_password, create_access_token, get_current_user, users_db, messages_db

router = APIRouter()

@router.post("/register")
async def register_user(username: str, password: str, role: str):
    if username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = get_password_hash(password)
    users_db[username] = User(id=username, username=username, role=role, hashed_password=hashed_password)
    return {"message": "User registered successfully"}

@router.post("/token", response_model=Token)
async def login_for_access_token(username: str, password: str):
    user = users_db.get(username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/send")
async def send_message(message: Message, current_user: User = Depends(get_current_user)):
    if message.sender_id not in users_db or message.receiver_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    messages_db.append(message)
    return {"message": "Message sent successfully"}

@router.get("/messages/{user_id}")
async def get_messages(user_id: str, current_user: User = Depends(get_current_user)):
    user_messages = [msg for msg in messages_db if msg.receiver_id == user_id]
    return {"messages": user_messages}
