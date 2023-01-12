from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    TIMESTAMP,

)

from src.auth.models import user

metadata = MetaData()


post = Table(
    "post",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("text", String, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("author_id", Integer, ForeignKey(user.c.id)),
)


like = Table(
    "like",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("post_id", Integer, ForeignKey(post.c.id)),
    Column("user_id", Integer, ForeignKey(user.c.id)),
)
