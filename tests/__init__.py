from data.endpoints import Endpoints
from data.generator.generator import Generator
from modules.registered_module import RegisteredModule
from utils.assertions import Assertions
from utils.schemas.registered_shema.request_schema import RegisteredRequestSchema
from utils.schemas.registered_shema.response_shema import TokenResponseSchema
from utils.vallidate import Validate

class Ab:

    generator = Generator()
    module = RegisteredModule()
    endpoint = Endpoints()
    validate = Validate()
    assertion = Assertions()

ctx = Ab()