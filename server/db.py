from starlette.authentication import BaseUser
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine("sqlite+aiosqlite:///db.db")
async_session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class User(Base, BaseUser):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    @property
    def is_authenticated(self) -> bool:
        return True

