import requests
from pprint import pprint


def test_get_books():
    url = "https://simple-books-api.click/books"
    response = requests.get(url)
    assert response.status_code == 200, "Некорректный статус код"
    pprint(response.json())
    pprint(response.headers) #возвращает заголовки
    pprint(response.ok) # все что ниже 400
    pprint(response.url)





