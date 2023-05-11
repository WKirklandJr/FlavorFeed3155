
def test_home_page(test_app):
    response = test_app.get('/recipes/new')
    response_data = response.data.decode('utf-8')

    assert '<label for="ingredients">Ingredients:</label>' in response_data
