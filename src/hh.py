import requests
from typing import List, Dict, Any

class Parser:
    """
    Родительский класс для парсеров
    """
    def __init__(self, file_worker: Any):
        self.file_worker = file_worker


class HH(Parser):
    """
    Класс для работы с API HeadHunter.

    Args:
        file_worker: Объект для работы с файлами, передаваемый родительскому классу Parser.
    """

    def __init__(self, file_worker: Any):
        """
        Инициализация класса HH.

        Args:
            file_worker (Any): Объект для работы с файлами.
        """
        self.url: str = 'https://api.hh.ru/vacancies'
        self.headers: Dict[str, str] = {'User-Agent': 'HH-User-Agent'}
        self.params: Dict[str, Any] = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies: List[Dict[str, Any]] = []
        super().__init__(file_worker)

    def load_vacancies(self, keyword: str):
        """
        Загрузка вакансий по ключевому слову.

        Args:
            keyword (str): Ключевое слово для поиска вакансий.
        """
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies: List[Dict[str, Any]] = response.json().get('items', [])
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
