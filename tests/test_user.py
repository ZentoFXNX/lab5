from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    data = {
        "name": "New User",
        "email": "new.user@mail.com"
    }
    response = client.post("/api/v1/user", json=data)
    assert response.status_code == 201
    assert isinstance(response.json(), int) 

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    data = {
        "name": "Duplicate User",
        "email": users[0]["email"] 
    }
    response = client.post("/api/v1/user", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    email = "delete.me@mail.com"
    client.post("/api/v1/user", json={"name": "Delete Me", "email": email})

    response = client.delete("/api/v1/user", params={"email": email})
    assert response.status_code == 204

    response = client.get("/api/v1/user", params={"email": email})
    assert response.status_code == 404