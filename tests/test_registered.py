import requests
from data.endpoints import Endpoints
from data.generator.generator import Generator
from modules.registered_module import RegisteredModule
from utils.assertions import Assertions
from utils.schemas.registered_shema.request_schema import RegisteredRequestSchema
from utils.schemas.registered_shema.response_shema import TokenResponseSchema
from utils.vallidate import Validate
from http import HTTPStatus as status


class TestRegistered:
    generator = Generator()
    module = RegisteredModule()
    endpoint = Endpoints()
    validate = Validate()
    assertion = Assertions()

    def test_registered(self):
        user_info = next(self.generator.registered_data())
        request_body = self.module.prepare_data(
            schema=RegisteredRequestSchema,
            data=user_info
        )
        """Пишем запрос"""
        response = requests.post(
            url= f"{self.endpoint.base_url}{self.endpoint.api_client_url}",
            data = request_body
        )
        self.validate.validate(
            response=response,
            shema= TokenResponseSchema
        )
        self.assertion.assert_status_code(
            response= response,
            status_code= status.CREATED
        )

