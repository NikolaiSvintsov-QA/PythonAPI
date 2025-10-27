import requests
from pydantic import BaseModel

"""Pydantic-Схемы - для тела запроса"""
class UserRegistrationSchema(BaseModel):
    clientName: str
    clientEmail: str

"""Pydantic-Схемы - для тела ответа"""
class TokenResponseSchema(BaseModel):
    accessToken: str

"""Создаем тест - c URL и тело запроса"""
def test_create_user():
    url = "https://simple-books-api.click/api-clients/"
    data = {
        "clientName": "Nfgeikoelaj344",
        "clientEmail": "Nikfer3ol43aj@yandex.ru"
    }

    """Отправляем POST запрос с параметрами URL и JSON"""
    response = requests.post(
        url=url,
        json=data
        )
    print(response.json())
    """Валидируем схема  тела  ответа"""
    try:
        TokenResponseSchema.model_validate(response.json())
    except ValueError as err:
        raise ValueError(f"Неверный формат тело ответа {err}")





