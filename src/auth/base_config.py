from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy
from fastapi_users import FastAPIUsers

from src.auth.manager import get_user_manager
from src.config import JWT_SECRET
from src.auth.models import User


SECRET = JWT_SECRET

cookie_transport = CookieTransport(cookie_name="simple-blog-token", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
