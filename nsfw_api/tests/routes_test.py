import json
import pytest
from nsfw_api import app


#Test cases for both POST and GET requests

def post_json(client, url, json_dict): 
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')


#def json_of_response(response):
#    """Decode json from response"""
#    return json.loads(response.data.decode('utf8'))


@pytest.fixture
def client(request):
    """Creating the test client for testing"""
    test_client = app.test_client()

    def teardown():
        pass 
    request.addfinalizer(teardown)
    return test_client


def test_dummy(client):
    response = client.get('/')
    assert b'Hello, World!' in response.data

def test_pred_get_nsfw_drawing(client):
    response = client.get('/pred?text=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRrgvEhxVsykGMqcDhwkqfiGKL7DeQtlrowuQ&usqp=CAU')
    assert response.status_code == 200
    assert float((json.loads(response.data))['Drawing']) >= 0.5

def test_pred_get_nsfw_hentai(client):
    response = client.get('/pred?text=https://disco.scrolller.com/media/5bfac.jpg')
    assert response.status_code == 200
    assert float((json.loads(response.data))['Hentai']) >= 0.4

def test_pred_get_nsfw_neutral(client):
    response = client.get('/pred?text=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTREGnw2J8IvE_m6wS1EF5-L7V8rjzg5RUSPw&usqp=CAU')
    assert response.status_code == 200
    assert float((json.loads(response.data))['Neutral']) >= 0.9

def test_pred_get_nsfw_porn(client):
    response = client.get('/pred?text=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRNaDfuRqSFThBAugXmOE7u5ITslLwQVwxC2Q&usqp=CAU')
    assert response.status_code == 200
    assert float((json.loads(response.data))['Porn']) >= 0.5

def test_pred_get_nsfw_sexy(client):
    response = client.get('/pred?text=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQPgfhq7ah14x-85-Jq5fjuucMKe3IQjXKw2w&usqp=CAU')
    assert response.status_code == 200
    assert float((json.loads(response.data))['Sexy']) >= 0.5

def test_pred_post_nsfw_drawing(client):
    data = {
        'text':'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRrgvEhxVsykGMqcDhwkqfiGKL7DeQtlrowuQ&usqp=CAU'
    }
    url = '/pred'
    response = client.post(url, data = data) 
    assert response.status_code == 200
    assert float((json.loads(response.data))['Drawing']) >= 0.5

def test_pred_post_nsfw_hentai(client):
    data = {
        'text': 'https://disco.scrolller.com/media/5bfac.jpg'
    }
    url = '/pred'
    response = client.post(url, data = data)
    assert response.status_code == 200
    assert float((json.loads(response.data))['Hentai']) >= 0.4

def test_pred_post_nsfw_neutral(client):
    data = {
        'text': 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTREGnw2J8IvE_m6wS1EF5-L7V8rjzg5RUSPw&usqp=CAU'
    }
    url = '/pred'
    response = client.post(url, data = data)
    assert response.status_code == 200
    assert float((json.loads(response.data))['Neutral']) >= 0.9

def test_pred_post_nsfw_porn(client):
    data = {
        'text': 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRNaDfuRqSFThBAugXmOE7u5ITslLwQVwxC2Q&usqp=CAU'
    }
    url = '/pred'
    response = client.post(url, data = data)
#    response = client.get('/pred?text=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRNaDfuRqSFThBAugXmOE7u5ITslLwQVwxC2Q&usqp=CAU')
    assert response.status_code == 200
    assert float((json.loads(response.data))['Porn']) >= 0.5

def test_pred_post_nsfw_sexy(client):
    data = {
        'text': 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQPgfhq7ah14x-85-Jq5fjuucMKe3IQjXKw2w&usqp=CAU'
    }
    url = '/pred'
    response = client.post(url, data = data)
#    response = client.get('/pred?text=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQPgfhq7ah14x-85-Jq5fjuucMKe3IQjXKw2w&usqp=CAU')
    assert response.status_code == 200
    assert float((json.loads(response.data))['Sexy']) >= 0.5




