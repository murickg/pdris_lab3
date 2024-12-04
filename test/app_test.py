import pytest
from unittest.mock import patch, MagicMock
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.app.db_create_table')  # Мокируем создание таблицы
def test_home(mock_create_table, client):
    mock_create_table.return_value = None  # Указываем, что функция ничего не возвращает
    response = client.get('/')
    assert response.status_code == 200
    assert "Welcome to the home page!" in response.get_json()["message"]
    mock_create_table.assert_called_once()  # Проверяем, что создание таблицы вызывалось

@patch('app.app.db_connection')  # Мокируем подключение к базе
def test_add_user_success(mock_db_connection, client):
    # Создаем мок для подключения и курсора
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/add_user', json={"name": "Murick", "last_name": "Gamzatov"})
    assert response.status_code == 201
    assert response.get_json()["message"] == "Entry added successfully"

    # Проверяем вызовы для базы данных
    mock_db_connection.assert_called_once()
    mock_cursor.execute.assert_called_once_with('INSERT INTO users (name, last_name) VALUES (%s, %s)', ('Murick', 'Gamzatov'))
    mock_conn.commit.assert_called_once()

@patch('app.app.db_connection')
def test_add_user_failure(mock_db_connection, client):
    response = client.post('/add_user', json={"name": "Murick"})
    assert response.status_code == 400
    assert "error" in response.get_json()
    assert response.get_json()["error"] == "The name and last_name fields are required"

    # Проверяем, что подключение к базе не вызывалось
    mock_db_connection.assert_not_called()

@patch('app.app.db_connection')
def test_get_users(mock_db_connection, client):
    # Создаем мок для подключения и курсора
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Мокируем данные из базы
    mock_cursor.fetchall.return_value = [
        (1, "Ivan", "Ivanov"),
        (2, "Iwan", "Iwanov")
    ]

    response = client.get('/get_users')
    assert response.status_code == 200
    users = response.get_json()["users"]
    assert len(users) == 2
    assert users[0]["name"] == "Ivan"
    assert users[1]["last_name"] == "Iwanov"

    # Проверяем вызовы для базы данных
    mock_db_connection.assert_called_once()
    mock_cursor.execute.assert_called_once_with('SELECT * FROM users')
