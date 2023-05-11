import pytest
from app import app
from src.models import db, User, Recipe, Tag, Bookmark, Comment

@pytest.fixture(scope='module')
def test_app():
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.drop_all()