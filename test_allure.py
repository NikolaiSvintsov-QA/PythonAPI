import requests
from pprint import pprint
import allure

@allure.epic("Test EPIC ")
class TestAllure:

    @allure.feature("Get books feature")
    @allure.story("Get books story")
    @allure.title("Get books title") # название теста
    @allure.description("Get books description") # описание теста
    @allure.severity(allure.severity_level.CRITICAL) # приоритет теста
    @allure.id("ID Test") # id теста
    @allure.link("https://github.com/vdespa/introduction-to-postman-course/blob/main/simple-books-api.md")
    def test_get_books(self):
        with allure.step("Step№1"):
            url = "https://simple-books-api.click/books"
        with allure.step('Step_2'):
            response = requests.get(url)
        with allure.step("assert that response status code equals 200"):
            assert response.status_code == 200, "Некорректный статус код"
        pprint(response.json())
        pprint(response.headers) #возвращает заголовки
        pprint(response.ok) # все что ниже 400
        pprint(response.url)








