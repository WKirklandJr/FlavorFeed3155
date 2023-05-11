from app import app
from src.repositories.recipe_repository import recipe_repository_singleton


def test_get_single_recipe(client):
     response = client.get("/recipes/1")
     assert "<h2 class="">" in response.data