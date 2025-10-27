import requests
from faker import Faker
from pydantic import BaseModel, Field
from dataclasses import dataclass

from typing_inspection.typing_objects import alias

faker = Faker()

"""Храним данные пользователя  """


@dataclass  # Декоратор (обозначаем что отвечает только за данные)
class UserData:
    clientNameData: str = None
    clientEmailData: str = None


"""Генерируем данные пользователя"""
def generate_user_data():
    yield UserData(
        clientNameData=faker.name(),
        clientEmailData=faker.email()
    )

"""Пишем тест проверка  test_generate_user_data генерировали данные и печатали их"""
def test_generate_user_data():
    user = next(generate_user_data())
    print(user)


"""Пишем тест №2 """
def test_generate_user_fake_data():
    user = next(generate_user_data())
    """Отправляем запрос на URL"""
    url = "https://simple-books-api.click/api-clients/"
    data = {
        "clientName": user.clientNameData,
        "clientEmail": user.clientEmailData
    }
    response = requests.post(
        url=url,
        json=data
    )
    assert response.status_code == 201, "Некорректный статус код"


# ---
"""Пробуем с Pydantic-Схемы """
"""Pydantic-Схемы - для тела запроса"""
class UserRegistrationSchema(BaseModel):
    client_name: str = Field(...,alias="clientName")
    client_email: str = Field(...,alias="clientEmail")

"""Pydantic-Схемы - для тела ответа"""
class TokenResponseSchema(BaseModel):
    accessToken: str


def test_generate_user_fake_data_schema_data():
    user = next(generate_user_data())
    """Отправляем запрос на URL"""
    url = "https://simple-books-api.click/api-clients/"
    data = UserRegistrationSchema(
        clientName=user.clientNameData,
        clientEmail=user.clientEmailData
    )
    """Перевод в из JSON  в data"""
    data = data.model_dump_json(by_alias = True)
    response = requests.post(
        url=url,
        data=data
    )
    assert response.status_code == 201, "Некорректный статус код"


def test_generate_user_fake_data_schema_json():
    user = next(generate_user_data())
    """Отправляем запрос на URL"""
    url = "https://simple-books-api.click/api-clients/"
    data = UserRegistrationSchema(
        clientName=user.clientNameData,
        clientEmail=user.clientEmailData
    )
    """Перевод в из JSON  в data"""
    data = data.model_dump(by_alias = True)
    response = requests.post(
        url=url,
        json=data
    )
    try:
        """Pydantic-Схемы - для тела ответа"""
        TokenResponseSchema.model_validate(response.json())
    except ValueError as err:
        raise ValueError(f" Какой-то {err}")





