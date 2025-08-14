from pydantic import BaseModel, Field
from typing import  Optional
from datetime import datetime

class PostCreate(BaseModel):
    title: str = Field(..., max_length=255)
    content: str

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    updated_at: datetime
    likes_count: int = 0
    comments_count: int = 0

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime

class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    

    class Config:
        orm_mode = True