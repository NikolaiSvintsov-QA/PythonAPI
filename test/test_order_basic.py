import requests
import pytest
from faker import Faker



faker = Faker()
BASE_URL = "https://simple-books-api.click"

"""Создаем тестовые данные"""
def generate_user_data():
    return {
        "clientName": faker.name(),
        "clientEmail": faker.email()
    }

def test_login():
    """1. Регистрируем клиента и проверяем, что получен токен."""
    response = requests.post(url=f"{BASE_URL}/api-clients/", json = generate_user_data())
    token = response.json().get("accessToken")
    assert response.status_code == 201, "Некорректный статус код при регистрации"
    assert token is not None, "Токен не получен"
    assert len(token) > 10, f"Токен подозрительно короткий: {token}"
    print("Токен успешно получен :", token)

def take_token():
    """Отдельная функция для получения токена(используем в других тестах)"""
    response = requests.post(url=f"{BASE_URL}/api-clients/", json=generate_user_data())
    assert response.status_code == 201, f"Ошибка при получении токена: {response.status_code}"
    token = response.json().get("accessToken")
    assert token, "Токен не найден в ответе"
    return token

def test_create_order():
    """2. Создаем ордер и проверяем, что он успешно создан."""
    token = take_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    customer_name = faker.name() # сохранили имя для проверки
    body_json = {
        "bookId": faker.random_int(min=1, max=6),
        "customerName": customer_name
    }
    response = requests.post(url=f"{BASE_URL}/orders", json=body_json, headers = headers )
    assert response.status_code == 201, f"Ошибка при создании ордера: {response.status_code} {response.text}"
    """Сохраняем тело ответа"""
    """
    1. Отправил запрос → пришёл JSON (строка) - Сервер прислал строку: '{"orderId": "123", "created": true}'
    2.data = response.json() # Теперь data = {"orderId": "123", "created": True}  ← словарь Python
    3.order_id = data.get("orderId")  # order_id = "123"  ← достали ЗНАЧЕНИЕ, а не ключ!
    """
    data = response.json()
    order_id = data.get("orderId")

    assert order_id, "Не получили orderId при создании ордера!"
    print(f'Ордер создан! ID: {order_id}')

    """Проверка через GET-запрос, что данные реально сохранились на сервере.Это интеграционная проверка, что сервер корректно обработал данные"""
    response_get = requests.get(url=f"{BASE_URL}/orders/{order_id}", headers=headers)
    assert response_get.status_code == 200, f" Ошибка при получении ордера: {response_get.status_code}" #Проверяет, что сервер вернул код 200 (успешное выполнение).

    """Превращает JSON-строку (которую прислал сервер) в словарь Python, теперь можем работать как со словарем, и достать значение записанное в ключе customerName"""
    data_get = response_get.json()
    myname = data_get.get("customerName")  #Со словаря data_get достаёт значение по ключу "customerName"
    assert myname == customer_name, "Не верное сохраненное имя" #Сравнивает имя, которое получил с сервера (myname), с именем, которое отправлял при создании (customer_name)
    print(f"Получил ордер обратно: {data_get}")
    print(f"Получил имя: {myname}")

    """Работаю с методом PATCH"""
    new_customer_name = faker.name()
    """update_body - новое имя"""
    update_body = {
        "customerName": new_customer_name
    }
    """Запрос patch - включает URL, новое имя, headers - как token """
    response_patch = requests.patch(url=f"{BASE_URL}/orders/{order_id}",json=update_body, headers=headers)
    assert response_patch.status_code == 204, "Неверный статус код, при обновлении заказа"
    print(response_patch.status_code)

    """GET запрос, для проверки что изменение применилось"""
    response_patch_get = requests.get(url=f"{BASE_URL}/orders/{order_id}", headers=headers)
    """Проверяем что статус код 200"""
    assert response_patch_get.status_code == 200, f"Ошибка статус кода, при проверки что изменение к имени применилось Patch-а {response_patch_get.status_code}"

    """Превращает JSON-строку в словарь Python,  достать значение записанное в ключе customerName после изменения имени """
    data_patch_get = response_patch_get.json()
    """Со словаря data_patch_get достаёт значение по ключу "customerName"""
    patch_name = data_patch_get.get("customerName")
    assert patch_name == new_customer_name, "При частичном изменении данные не сохранились. "
    print(f"Получил новое имя : {patch_name} ")

    """Работаем с методом DELETE"""
    response_delete = requests.delete(url=f"{BASE_URL}/orders/{order_id}", headers=headers)
    """Проверим, что запрос приходит 204"""
    assert response_delete.status_code == 204, "Неверный статус код, при использовании метод 204"

    response_delete_get = requests.get(url=f"{BASE_URL}/orders/{order_id}", headers=headers)
    print(response_delete_get)
    """Проверка, что прейдет статус код 404"""
    assert response_delete_get.status_code == 404, "Ордер должен быть удален (404)"





