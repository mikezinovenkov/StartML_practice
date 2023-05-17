from sqlalchemy import Column, Integer, String, func, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base, SessionLocal
from table_post import Post
from table_user import User


class Feed(Base):
    __tablename__ = "feed_action"
    action = Column(String)
    post_id = Column(Integer, ForeignKey(Post.id), primary_key=True)
    post = relationship("Post")
    time = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    user = relationship("User")



    
    