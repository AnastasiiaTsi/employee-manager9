import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from employee_manager.models import Base
from employee_manager.dependencies import get_session
from employee_manager.api import app

@pytest.fixture
def session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine, expire_on_commit=False)
    with TestSession() as session:
        yield session
    Base.metadata.drop_all(engine)

@pytest.fixture
def session_override(session: Session):
    def _get_session_override():
        yield session
    app.dependency_overrides[get_session] = _get_session_override
    yield session
    app.dependency_overrides.clear()