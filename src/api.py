import requests
from abc import ABC, abstractmethod
from typing import List, Dict

class BaseAPI(ABC):
    """
    Абстрактный базовый класс для API.

    Определяет метод get_vacancies, который должен быть реализован в подклассах.
    """
    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, str]]:
        """
        Получает вакансии по заданному ключевому слову.

        :param keyword: Ключевое слово для поиска вакансий.
        :return: Список словарей с данными о вакансиях.
        """
        pass

class HHApi(BaseAPI):
    """
    Класс для взаимодействия с API HeadHunter.

    Используется для поиска вакансий по заданному ключевому слову.
    """
    def __init__(self):
        """
        Инициализация HHApi.

        Устанавливает URL и параметры по умолчанию для запросов.
        """
        self.url: str = "http://api.hh.ru/vacancies/"
        self.params: Dict[str, str] = {'text': '', 'page': 0, 'per_page': 100}

    def get_vacancies(self, keyword: str) -> List[Dict[str, str]]:
        """
        Получает вакансии по заданному ключевому слову.

        :param keyword: Ключевое слово для поиска вакансий.
        :return: Список словарей с данными о вакансиях.
        """
        self.params.update({'text': keyword})
        response = requests.get(self.url, params=self.params)
        return response.json()["items"]

if __name__ == "__main__":
    my_api: HHApi = HHApi()
    response: List[Dict[str, str]] = my_api.get_vacancies("крановщик")
    print(response)

