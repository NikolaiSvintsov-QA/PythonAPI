import requests
from pydantic import BaseModel, Field, ValidationError
from faker import Faker


faker = Faker()
BASE_URL = "https://simple-books-api.click"

""" Pydantic-схема ответа - Схема Токена"""
class TokenSchema(BaseModel):
    access_token :str = Field(..., alias="accessToken")

"""Pydantic-схема для ответа от API(ордер)"""
class OrderResponseSсhema(BaseModel):
    orderId: str
    created: bool

def get_token()->str:
    """Собираем тело запроса"""
    body = {
        "clientName": faker.user_name(),
        "clientEmail": faker.unique.email()
    }
    print(f"Тело запроса для создания клиента: {body}")
    """Отправляем запрос"""
    response = requests.post(f"{BASE_URL}/api-clients/", json=body)
    print(f"Ответ от API при создании клиента: {response.status_code} - {response.text}")  # Принт ответа
    """Статус - guard"""
    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"Ошибка при создании клиента:"
            f"{response.status_code} - {response.text} "
        )

    """Валидация схемы через Pydantic"""
    try:
        """Извлечение токена"""
        token = TokenSchema.model_validate(response.json())
        print("Токен успешно создан: ", token.access_token)
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")  # Принт ошибки валидации
        raise ValueError(f"Не формат ответа: {e}")

    # Извлечение и sanity-check
    token_str = token.access_token
    if not isinstance(token_str, str) or not token_str.strip():
        raise ValueError("Пустой access_token")

    return token_str



"""Создание ордера"""
def create_order(token:str):
    headers = {
        "Authorization":f"Bearer {token}"
    }
    order_url = f"{BASE_URL}/orders/"
    body_order = {
        "bookId": 1,
        "customerName": "John Doe" #
    }
    print(f"Тело запроса для создания ордера: {body_order}")  # Принт тела запроса
    response = requests.post(order_url, headers=headers, json=body_order)
    print(f"Ответ от API при создании ордера: {response.status_code} - {response.text}")  # Принт ответа
    if response.status_code !=201:
        raise RuntimeError(f"Ошибка при создании ордера: {response.status_code}-{response.text}")

    #Валидация ответа через Pydantic
    try:
        order_response = OrderResponseSсhema.model_validate(response.json())
        print(f"ID ордера получен: {order_response.orderId}")  # Принт полученного orderId
        return order_response.orderId # Возвращает ID ордера
    except ValidationError as e:
        raise ValueError(f'Ошибка формата ответа при создании ордера: {e}')


"""Создаем функцию get_order - которая отправляет запрос по адресу GET /orders/{orderId}"""
"""В параметры  так же добавим (token и ордер) """
def  get_order(token:str, order_id:str):
    """Получение информации об ордере по ID"""
    # 1. Создаем заголовок для запроса
    headers = {
        "Authorization": f"Bearer {token}"
    }
    print(f"[DEBUG] Заголовки запроса: {headers}")  # выводим, что у нас в headers
    response = requests.get(url=f"{BASE_URL}/orders/{order_id}", headers=headers)
    # 3) Что получили
    print(f"[DEBUG] Status: {response.status_code}")
    print(f"[DEBUG] Raw body: {response.text!r}")
    print(f"[DEBUG] Content-Type: {response.headers.get('Content-Type')}")
    # Проверяем статус
    if response.status_code != 200:
        raise RuntimeError(f"Ошибка при получении ордера: {response.status_code} - {response.text}")




""" Блок, который выполняется только при прямом запуске файла"""
if __name__ == "__main__":
    token = get_token()
    print("ОК, токен:", token)

    order_id = create_order(token)   # Создаём ордер, передавая токен
    print(f"Ордер успешно создан с orderId: {order_id} ")

    """Вызов функции get_order"""
    order_data = get_order(token,order_id)
    print(f"[DEBUG] Данные ордера: {order_data}")






