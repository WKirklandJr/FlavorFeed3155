
def test_home_page(test_app):
    response = test_app.get('/register')
    response_data = response.data.decode('utf-8')

    assert '<button class="btn btn-light  btn-block" type="button">Sign Up with Google</button>' in response_data
