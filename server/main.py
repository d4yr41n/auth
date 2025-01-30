from base64 import b64decode
from binascii import Error
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, requires
)
from starlette.endpoints import HTTPEndpoint
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response
from starlette.requests import Request
from starlette.routing import Route
from sqlalchemy import select

from db import Base, User, async_session, engine


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        async with async_session() as session:
            user = await session.scalar(
                select(User)
                .where(User.name == username, User.password == password)
            )
            if user:
                return AuthCredentials(["authenticated"]), user


class UserEndpoint(HTTPEndpoint):
    @requires("authenticated")
    async def get(self, request):
        async with async_session() as session:
            users = [
                {
                    "id": user.id,
                    "name": user.name
                }
                for user in await session.scalars(select(User))
            ]
        return JSONResponse(users)


@requires("authenticated")
def auth(request: Request):
    user = request.user
    return JSONResponse({                    
        "id": user.id,
        "name": user.name
    })


async def register(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.name == username))
        if not user:
            session.add(User(name=username, password=password))
            await session.commit()
            return Response()
    return Response(status_code=400)


async def login(request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    async with async_session() as session:
        user = await session.scalar(
            select(User)
            .where(User.name == username, User.password == password)
        )
        if user:
            return Response()
    return Response(status_code=400)


routes = [
    Route("/auth", auth),
    Route("/register", register, methods=["POST"]),
    Route("/login", login, methods=["POST"]),
    Route("/users", UserEndpoint)
]

middleware = [
    Middleware(CORSMiddleware,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_headers=["*"]
    ),
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]


@asynccontextmanager
async def lifespan(app: Starlette):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = Starlette(routes=routes, middleware=middleware, lifespan=lifespan)
