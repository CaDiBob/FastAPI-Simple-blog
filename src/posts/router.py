from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func, column, table

from src.auth.models import User
from src.database import get_async_session
from src.posts.models import post, like
from src.posts.schemas import PostCreate, PostEdit, ErrorMessage, Like
from src.auth.base_config import fastapi_users


current_user = fastapi_users.current_user()
router = APIRouter(
    prefix="/posts",
    tags=["post"]
)


@router.get("/")
async def get_posts(session: AsyncSession = Depends(get_async_session)):

    query = select(post)
    result = await session.execute(query)
    return result.all()


@router.get("/{post_id}")
async def get_post(post_id: int,
                   session: AsyncSession = Depends(get_async_session)):

    query = select(post).where(post.c.id == post_id)
    result = await session.execute(query)
    return result.first()


@router.post("/", responses={401: {"model": ErrorMessage}})
async def add_post(new_post: PostCreate,
                   session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):

    new_post = new_post.dict()
    new_post["author_id"] = user.id
    stmt = insert(post).values(**new_post)
    await session.execute(stmt)
    await session.commit()
    return new_post


@router.put("/{post_id}",
            response_model=PostEdit,
            responses={403: {"model": ErrorMessage},
                       401: {"model": ErrorMessage}})
async def update_post(post_id: int,
                      edited_post: PostEdit,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):

    query = select(post).where(post.c.id == post_id)\
        .where(post.c.author_id == user.id)
    result = await session.execute(query)
    if not result.first():
        return JSONResponse(content={"message": "Forbidden"}, status_code=403)

    stmt = update(post).where(post.c.id == post_id)\
        .where(post.c.author_id == user.id)\
        .values(**edited_post.dict())
    await session.execute(stmt)
    await session.commit()
    return edited_post


@router.delete("/posts",
               responses={403: {"model": ErrorMessage},
                          401: {"model": ErrorMessage}})
async def delete_post(post_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):

    query = select(post).where(post.c.id == post_id)\
        .where(post.c.author_id == user.id)
    result = await session.execute(query)
    if not result.first():
        return JSONResponse(content={"message": "Forbidden"}, status_code=403)

    stmt = delete(post).where(post.c.id == post_id).where(post.c.author_id == user.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "post deleted"}


@router.post("/{post_id}/like", responses={409: {"model": ErrorMessage}})
async def add_like(post_id: int,
                   new_like: Like,
                   session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    query = select(like).where(like.c.user_id == user.id).where(like.c.post_id == post_id)
    result = await session.execute(query)
    if result.first():
        return JSONResponse(content={"message": "Conflict - post already like"}, status_code=409)
    query = select(post.c.author_id).where(post.c.id == post_id)
    result = await session.execute(query)
    author_id, *_ = result.first()
    if author_id == user.id:
        return JSONResponse(content={"message": "Conflict - this post is own"}, status_code=409)

    new_like = new_like.dict()
    new_like["post_id"] = post_id
    new_like["user_id"] = user.id
    stmt = insert(like).values(**new_like)
    await session.execute(stmt)
    await session.commit()
    return {"status": "like post"}


@router.delete("/{post_id}/like", responses={409: {"model": ErrorMessage}})
async def remove_like(post_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    query = select(like).where(like.c.post_id == post_id).where(like.c.user_id == user.id)
    result = await session.execute(query)
    if not result.first():
        return JSONResponse(content={"message": "Conflict - post not like yet"}, status_code=409)

    stmt = delete(like).where(like.c.post_id == post_id).where(like.c.user_id == user.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "like remove"}
