from functools import wraps
from loguru import logger

"""С начало очищаем все логи"""
logger.remove()
"""Добавляем логи, в определенном формате """
logger.add(
    sink=r"/Users/paur/PycharmProjects/pythonAPI/logs.log",
    level="INFO",
    format="{time:YYYY-MM-DD} | {level} | {message}",
    rotation="10MB",
    retention="10 days"
)
"""Логи собираются в определённый файл"""
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} успешно выполнена с результатом: {result}")
            return result
        except Exception as e:
            logger.error(f"Ошибка в {func.__name__} : {str(e)}")
            raise
    return wrapper

