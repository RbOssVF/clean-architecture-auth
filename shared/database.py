from sqlmodel import create_engine, Session
from .config import settings
from contextlib import asynccontextmanager
from contextvars import ContextVar

engine = create_engine(
    settings.DATABASE_URL,
    echo=False
)

_session_var: ContextVar[Session] = ContextVar("session")

def get_session() -> Session:
    return _session_var.get()

@asynccontextmanager
async def in_transaction():
    with Session(engine) as session:
        token = _session_var.set(session)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            _session_var.reset(token)

@asynccontextmanager
async def simple_session():
    with Session(engine) as session:
        token = _session_var.set(session)
        try:
            yield session
        finally:
            _session_var.reset(token)
