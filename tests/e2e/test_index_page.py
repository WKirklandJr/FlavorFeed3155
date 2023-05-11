
def test_home_page(test_app):
    response = test_app.get('/')
    response_data = response.data.decode('utf-8')

    assert '<h5>CONTACT US</h5>' in response_data
