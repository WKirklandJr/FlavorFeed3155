import pytest
from app import app, session

from flask import Blueprint, session, render_template, request, redirect, abort
from src.models import db
from src.repositories.user_repository import user_repository_singleton
from src.repositories.recipe_repository import recipe_repository_singleton



from src.models import User, Recipe

@pytest.fixture(scope='session')
def test_app():
    return app.test_client()

def login(test_app, email, username, password):
    return test_app.post('/login', data=dict(email=email,
        username=username,
        password=password
    ), follow_redirects=True)


def logout():
    return test_app.get('/logout', follow_redirects=True)

@pytest.fixture(scope='session')
def create_user():
    testuser = User('test@example.com', 'testuser', 'password123')
    return testuser


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()