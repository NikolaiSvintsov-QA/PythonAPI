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

"""Pydantic OrderSchema"""
class OrderSchema(BaseModel):
    id: str
    bookId:int
    customerName:str
    quantity:int
    timestamp:int

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
def create_order(token:str)->str:
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
def  get_order(token: str, order_id: str)-> dict:
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

    """Ловит все возможные ошибки по формирование ошибок"""
    try:
        data = response.json()
        print(f"[DEBUG] Распарсенные данные: {data}")
        validated = OrderSchema.model_validate(data)
        print(f"[DEBUG] Validated: {validated}")
        return validated.model_dump() ## ← возвращаем уже проверенный dict
    except Exception as e:
        print(f"[ERROR] Не удалось обработать ответ как JSON.")
        print(f"[ERROR] Код: {response.status_code}")
        print(f"[ERROR] Заголовки: {response.headers}")
        print(f"[ERROR] Тело ответа (первые 200 символов): {response.text[:200]!r}")
        print(f"[ERROR] Детали исключения: {type(e).__name__}-{e}")
        raise # Пробрасываем ошибку дальше, чтобы не скрывать проблему

"""Проверяем что наш сервер жив"""
def get_status():
    response_get_status = requests.get(url=f"{BASE_URL}/status")
    response_body = response_get_status.json()
    return response_body

"""Создаю вспомогательную функцию  headers:с токеном чтоб каждый раз не прописывать"""
def get_headers(token:str)-> dict:
    return {"Authorization": f"Bearer {token}"}


def patch_method(token: str, order_id: str, new_name: str) -> dict | None:

    """
    Частично обновляет заказ: меняет customerName у конкретного order_id.
    Требует Bearer-токен (в headers_def или через token).
    Возвращает JSON-ответ сервера (обычно короткое подтверждение).
    """
    headers = get_headers(token)
    headers["Content-Type"] = "application/json" #добавляем еще один заголовок
    url = f"{BASE_URL}/orders/{order_id}"
    body = {"customerName": new_name}
    response_patch = requests.patch(url, headers=headers, json=body)
    print(f"[DEBUG] Status: {response_patch.status_code}")
    print(f"[DEBUG] Body: {response_patch.text}")
    if response_patch.status_code not in (200, 204):
        raise RuntimeError(
            f"Ошибка при обновлении ордера: "
            f"{response_patch.status_code} - {response_patch.text}"
        )
        # Если 204 — тела нет. Если 200 — вернём JSON.
    if response_patch.status_code == 204 or not response_patch.text.strip():
        return None
    return response_patch.json()






""" Блок, который выполняется только при прямом запуске файла"""
if __name__ == "__main__":
    token = get_token()
    print("ОК, токен:", token)

    order_id = create_order(token)   # Создаём ордер, передавая токен
    print(f"Ордер успешно создан с orderId: {order_id} ")

    """Вызов функции get_order"""
    order_data = get_order(token , order_id)
    print(f"[DEBUG] Данные ордера: {order_data}")
    assert str(order_data.get("id")) == str(order_id), f"id не совпал: {order_data}"

    """Получаем код что сервер живой"""
    get_body = get_status()
    print(f"[DEBUG] Получает ответ от сервера : {get_body}")

    headers_def = get_headers(token)
    print(f"[DEBUG] Headers вынесен в функцию и он такой : {headers_def}")

    patch_resp = patch_method(token, order_id, "QA Renamed")
    print("[DEBUG] PATCH resp:", patch_resp)

    # 3) Подтверждаем, что имя реально поменялось
    order_after = get_order(token, order_id)
    print("[DEBUG] After PATCH:", order_after)
    assert order_after["customerName"] == "QA Renamed", "Имя не обновилось"








