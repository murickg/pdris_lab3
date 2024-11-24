import pytest
from app.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Welcome to the home page!" in response.get_json()["message"]


def test_add_user_success(client):
    response = client.post('/add_user', json={"name": "Murick", "last_name": "Gamzatov"})
    assert response.status_code == 201
    assert response.get_json()["message"] == "Entry added successfully"


def test_add_user_failure(client):
    response = client.post('/add_user', json={"name": "Murick"})
    assert response.status_code == 400
    assert "error" in response.get_json()
    assert response.get_json()["error"] == "The name and last_name fields are required"


def test_get_users(client):
    # Добавляем пользователя
    client.post('/add_user', json={"name": "Ivan", "last_name": "Ivanov"})
    client.post('/add_user', json={"name": "Iwan", "last_name": "Iwanov"})

    # Проверяем список пользователей
    response = client.get('/get_users')
    assert response.status_code == 200
    users = response.get_json()["users"]
    assert len(users) >= 2
    assert users[0]["name"] == "Ivan"
    assert users[1]["last_name"] == "Iwanov"
