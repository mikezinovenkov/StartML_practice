from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
from table_post import Post
from table_user import User
from table_feed import Feed
from schema import UserGet, PostGet, FeedGet


# uvicorn app:app --reload --port 8899

app = FastAPI()


def get_db():
    with SessionLocal() as db:
        return db


@app.get("/user/{id}", response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):

    result = db.query(User).filter(User.id == id).one_or_none()

    if result == None:
        raise HTTPException(404, "user not found")
    else:
        return result


@app.get("/post/{id}", response_model=PostGet)
def get_post(id: int, db: Session = Depends(get_db)):
    
    result = db.query(Post).filter(Post.id == id).one_or_none()

    if result == None:
        raise HTTPException(404, "post not found")
    else:
        return result


@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_users_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):

    return db.query(Feed)\
            .join(User)\
            .filter(User.id == id)\
            .order_by(Feed.time.desc())\
            .limit(limit)\
            .all()


@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_posts_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    
    return db.query(Feed)\
            .join(Post)\
            .filter(Post.id == id)\
            .order_by(Feed.time.desc())\
            .limit(limit)\
            .all()


@app.get("/post/recommendations/")
def get_recommended_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    
    return db.query(Post)\
            .select_from(Feed)\
            .join(Post)\
            .filter(Feed.action == 'like')\
            .group_by(Post.id)\
            .order_by(func.count(Feed.post_id).desc())\
            .limit(limit)\
            .all()

