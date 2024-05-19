import requests
from abc import ABC, abstractmethod


class BaseAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword, count):
        pass

class HHApi(BaseAPI):
    def __init__(self):
        self.url = "http://api.hh.ru/vacancies/"
        self.params = {'text': '', 'page': 0, 'per_page': 100}

    def get_vacancies(self, keyword, count):
        self.params.update({"text": keyword})
        responce = requests.get(self.url, params=self.params)
        pass


if __name__ == "__main__":
    my_api = HHApi()
    responce = my_api.get_vacancies("крановщик", 100)