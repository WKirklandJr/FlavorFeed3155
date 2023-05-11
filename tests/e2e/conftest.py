import pytest
from app import app
from src.models import db, User, Recipe, Tag, Bookmark, Comment

@pytest.fixture(scope='module')
def test_app():
    return app.test_client()