from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, get_db, Base
from app.models import Post, User
from app.schemas import PostCreate, PostResponse
import logging

Base.metadata.create_all(bind=engine)


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

app = FastAPI(title="Blog API", version="1.0")


@app.get("/posts", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


@app.post("/posts", response_model=PostResponse, status_code=201)
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    post = Post(**post_data.model_dump(), author_id=1)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/users/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.posts
