import pytest
from app import app, session

from flask import Blueprint, session, render_template, request, redirect, abort
from src.models import db
from src.repositories.user_repository import user_repository_singleton
from src.repositories.recipe_repository import recipe_repository_singleton



from src.models import User, Recipe

@pytest.fixture(scope='module')
def test_app():
    return app.test_client()




@pytest.fixture()
def runner(app):
    return app.test_cli_runner()