from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import jwt
import datetime
import os

app = FastAPI()

# Database connection
db_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = db_client["my_database"]
users_collection = db["users"]
posts_collection = db["posts"]

# JWT settings
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model
class User(BaseModel):
    username: str
    password: str

# Post model
class Post(BaseModel):
    title: str
    content: str

# Create a new user
@app.post("/users/", response_model=User)
async def create_user(user: User):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    await users_collection.insert_one(user_dict)
    return user

# Login user
@app.post("/token/", response_model=dict)
async def login(user: User):
    existing_user = await users_collection.find_one({"username": user.username})
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not pwd_context.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    payload = {"sub": existing_user["username"], "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# Get the current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Create a new post
@app.post("/posts/", response_model=Post)
async def create_post(post: Post, current_user: str = Depends(get_current_user)):
    post_dict = post.dict()
    post_dict["username"] = current_user
    await posts_collection.insert_one(post_dict)
    return post

# Read a post
@app.get("/posts/{post_id}", response_model=Post)
async def read_post(post_id: str, current_user: str = Depends(get_current_user)):
    post = await posts_collection.find_one({"_id": post_id})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post["username"] != current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    return post

# Update a post
@app.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: str, post: Post, current_user: str = Depends(get_current_user)):
    existing_post = await posts_collection.find_one({"_id": post_id})
    if existing_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if existing_post["username"] != current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    post_dict = post.dict()
    post_dict["username"] = current_user
    await posts_collection.update_one({"_id": post_id}, {"$set": post_dict})
    return post

# Delete a post
@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, current_user: str = Depends(get_current_user)):
    existing_post = await posts_collection.find_one({"_id": post_id})
    if existing_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if existing_post["username"] != current_user:
        raise HTTPException(status_code=401, detail="Not authorized")
    await posts_collection.delete_one({"_id": post_id})
    return {"message": "Post deleted successfully"}