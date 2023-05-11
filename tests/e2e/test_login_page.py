
def test_home_page(test_app):
    response = test_app.get('/login')
    response_data = response.data.decode('utf-8')

    assert '<a class="small text-warning" href="#!">Forgot password?</a>' in response_data
