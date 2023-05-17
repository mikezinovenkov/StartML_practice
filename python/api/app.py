from fastapi import FastAPI, HTTPException, Depends
import datetime
from pydantic import BaseModel
from loguru import logger
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List


app = FastAPI()




@app.get("/sum_date")
def sum_date(current_date: datetime.date, offset: int):
    return current_date + datetime.timedelta(offset)


class User(BaseModel):
    name : str
    surname : str
    age : int
    registration_date : datetime.date

    class Config:
         orm_mode = True

@app.post("/users/validate")
def validate_user(user: User):
    return f"Will add user: {user.name} {user.surname} with age {user.age}"



class User_id(BaseModel):
    id : int
    gender : bool
    age : int
    city : str

    class Config:
         orm_mode = True

def get_db():
    conn = psycopg2.connect(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml",
        cursor_factory=RealDictCursor
    )
    return conn

@app.get("/user/{id}")
def get_info(id : int, conn = Depends(get_db)):

    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT id, gender, city
        FROM "user"
        WHERE id = {id}
        """
    )
    result = cursor.fetchone()

    if result == None:
        raise HTTPException(404, "user not found")
    else:
        return result



class PostResponse(BaseModel):

    id : int
    text : str
    topic : str

    class Config:
         orm_mode = True


@app.get("/post/{id}", response_model=PostResponse)
def get_info(id : int, conn = Depends(get_db)) -> PostResponse:

    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT id, text, topic
        FROM "post"
        WHERE id = {id}
        """
    )
    result = cursor.fetchone()

    if result == None:
        raise HTTPException(404, "user not found")
    else:
        return PostResponse(**result)