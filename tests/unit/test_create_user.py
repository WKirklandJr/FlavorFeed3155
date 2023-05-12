from src.repositories.user_repository import user_repository_singleton
from app import app
from src.models import db, User

def test_create_user():
    with app.app_context():
        db.session.query(User).delete()
        db.session.commit()

        user = user_repository_singleton.create_user('test@example.com', 'testuser', 'password123')
        
        assert user.email == 'test@example.com'
        assert user.username == 'testuser'
        assert user.password == 'password123'
        
    