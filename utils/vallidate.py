from utils.logger import log


class Validate:
    @log
    def validate(self, response, shema):
        """
        Валидирует тело ответа на основании переданной схемы
        :param response: тело ответа
        :param shema: схема для валидации
        :return: bool
        """
        try:
            shema.model_validate(response.json())
        except ValueError as e:
            raise ValueError(f"Invalid response format in {e}")