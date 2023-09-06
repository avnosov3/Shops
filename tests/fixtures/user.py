import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(name='client', scope='session')
def client():
    with TestClient(app) as client:
        yield client
