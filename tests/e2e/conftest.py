import pytest
from app import app
from src.models import db, User, Tag, Bookmark, Recipe, Comment


@pytest.fixture(scope='module')
def test_app():
    with app.app_context():
        Recipe.query.delete()
        db.session.commit()
        yield app.test_client()
