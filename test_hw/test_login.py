import json

import requests
import pytest
import faker



faker = faker.Faker()
BASE_URL = "https://simple-books-api.click"

"""Создаем тестовые данные"""
def generate_user_data():
    return {
        "clientName": faker.name(),
        "clientEmail": faker.email()
    }

def test_login():
    response = requests.post(url=f"{BASE_URL}/api-clients/", json = generate_user_data())
    token = response.json().get("accessToken")
    assert response.status_code == 201, "Некорректный статус код при регистрации"

def take_token():
    response = requests.post(url=f"{BASE_URL}/api-clients/", json=generate_user_data())
    token = response.json().get("accessToken")
    return token

def test_create_order():
    token = take_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body_json = {
        "bookId": faker.random_int(min=1, max=6),
        "customerName": faker.name()
    }
    response = requests.post(url=f"{BASE_URL}/orders", json=body_json, headers = headers )
    print(response.json())
    print(response.status_code)





















