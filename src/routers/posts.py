from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List

from src.configs.config import get_db
from src.schemas.post import *
from src.services.tables import Tables
from src.utils.token import get_current_user

router = APIRouter()
tables = Tables()


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    try:
        insert_stmt = (
            insert(tables.posts)
            .values(title=post.title, content=post.content, author_id=user)  # ✅ user is an int now
            .returning(tables.posts)
        )
        result = db.execute(insert_stmt)
        db.commit()
        new_post = result.fetchone()
        if not new_post:
            raise HTTPException(status_code=500, detail="Failed to create post")
        return new_post
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create post")


@router.get("/", response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    try:
        query = select(tables.posts)
        posts = db.execute(query).mappings().all()

        posts_with_counts = []
        for post in posts:
            likes_count = db.execute(
                select(func.count()).select_from(tables.likes).where(tables.likes.c.post_id == post.id)
            ).scalar()
            comments_count = db.execute(
                select(func.count()).select_from(tables.comments).where(tables.comments.c.post_id == post.id)
            ).scalar()
            post_dict = dict(post)
            post_dict.update({"likes_count": likes_count, "comments_count": comments_count})
            posts_with_counts.append(post_dict)
        return posts_with_counts
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to fetch posts")


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    query = select(tables.posts).where(tables.posts.c.id == post_id)
    post = db.execute(query).mappings().fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    likes_count = db.execute(
        select(func.count()).select_from(tables.likes).where(tables.likes.c.post_id == post_id)
    ).scalar()
    comments_count = db.execute(
        select(func.count()).select_from(tables.comments).where(tables.comments.c.post_id == post_id)
    ).scalar()

    post_dict = dict(post)
    post_dict.update({"likes_count": likes_count, "comments_count": comments_count})
    return post_dict



@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Check ownership
    query = select(tables.posts).where(
        (tables.posts.c.id == post_id) & (tables.posts.c.author_id == user)
    )
    existing_post = db.execute(query).fetchone()
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")

    update_values = {}
    if post_data.title is not None:
        update_values["title"] = post_data.title
    if post_data.content is not None:
        update_values["content"] = post_data.content

    if not update_values:
        raise HTTPException(status_code=400, detail="No data provided for update")

    try:
        update_stmt = (
            update(tables.posts)
            .where(tables.posts.c.id == post_id)
            .values(**update_values)
            .returning(tables.posts)
        )
        result = db.execute(update_stmt)
        db.commit()
        updated_post = result.fetchone()
        return updated_post
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update post")


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = select(tables.posts).where(
        (tables.posts.c.id == post_id) & (tables.posts.c.author_id == user)
    )
    post = db.execute(query).mappings().fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")

    try:
        delete_stmt = delete(tables.posts).where(tables.posts.c.id == post_id)
        db.execute(delete_stmt)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Post deleted successfully"})
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete post")







@router.post("/{post_id}/comment")
def add_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    user: int = Depends(get_current_user)
):
    # Check if post exists
    post_query = select(tables.posts).where(tables.posts.c.id == post_id)
    post = db.execute(post_query).fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Insert new comment
    insert_stmt = insert(tables.comments).values(
        post_id=post_id,
        user_id=user,    
        content=comment.content
    )
    db.execute(insert_stmt)
    db.commit()

    return {"detail": "Comment added successfully"}



@router.get("/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    # Check if post exists
    post_query = select(tables.posts).where(tables.posts.c.id == post_id)
    post = db.execute(post_query).fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Get comments for the post
    comments_query = select(tables.comments).where(tables.comments.c.post_id == post_id)
    comments = db.execute(comments_query).mappings().all() 

    return comments



@router.post("/{post_id}/like")
def like_post(post_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    post_query = select(tables.posts).where(tables.posts.c.id == post_id)
    post = db.execute(post_query).fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    like_query = select(tables.likes).where(
        (tables.likes.c.post_id == post_id) & (tables.likes.c.user_id == user)
    )
    existing_like = db.execute(like_query).fetchone()
    if existing_like:
        raise HTTPException(status_code=400, detail="You have already liked this post")

    insert_stmt = insert(tables.likes).values(post_id=post_id, user_id=user)
    db.execute(insert_stmt)
    db.commit()

    return {"detail": "Post liked successfully"}
