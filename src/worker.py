import os
from typing import List, Dict
import json
from src.api import HHApi
from src.vacancy import Vacancy
from config import DATA_PATH
from abc import abstractmethod, ABC


class BaseWorker(ABC):
    """
    Абстрактный базовый класс для работы с вакансиями.
    """

    @abstractmethod
    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        """
        Добавить список вакансий.

        :param vacancies: Список объектов вакансий.
        """
        pass

    @abstractmethod
    def del_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удалить вакансию.

        :param vacancy: Объект вакансии для удаления.
        """
        pass

    @abstractmethod
    def select_vacancy(self, keyword: str) -> List[Vacancy]:
        """
        Выбрать вакансии по ключевому слову.

        :param keyword: Ключевое слово для поиска вакансий.
        :return: Список объектов вакансий.
        """
        pass


class JSONWorker(BaseWorker):
    """
    Класс для работы с вакансиями в формате JSON.
    """

    def __init__(self, file_name: str) -> None:
        """
        Инициализация JSONWorker с именем файла.

        :param file_name: Имя файла для хранения вакансий.
        """
        self.file_path: str = os.path.join(DATA_PATH, file_name)
        self.prepare()

    def prepare(self) -> None:
        """
        Подготовка файла JSON: создание или очистка.
        """
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)
        else:
            open(self.file_path, "w").close()
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        """
        Добавить список вакансий в файл JSON.

        :param vacancies: Список объектов вакансий.
        """
        with open(self.file_path, encoding="utf-8") as f:
            json_data: List[Dict[str, str]] = json.load(f)
            for vacancy in vacancies:
                new_dict: Dict[str, str] = {
                    "title": vacancy.title,
                    "url": vacancy.url,
                    "salary_from": str(vacancy.salary_from),
                    "salary_to": str(vacancy.salary_to),
                    "requirements": vacancy.requirements,
                    "responsibility": vacancy.responsibility,
                    "city": vacancy.city
                }
                json_data.append(new_dict)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def return_list_vacancies(self) -> List[Vacancy]:
        """
        Вернуть список вакансий из файла JSON.

        :return: Список объектов вакансий.
        """
        with open(self.file_path, encoding="utf-8") as f:
            json_data: List[Dict[str, str]] = json.load(f)
            selected_vacancies: List[Vacancy] = []
            for item in json_data:
                vacancy = Vacancy(
                    item["title"],
                    item["url"],
                    int(item["salary_from"]),
                    int(item["salary_to"]),
                    item["requirements"],
                    item["responsibility"],
                    item["city"]
                )
                selected_vacancies.append(vacancy)
        return selected_vacancies

    def del_vacancy(self, vacancy: object):
        """
        Удалить вакансию из файла JSON.

        :param vacancy: Объект вакансии для удаления.
        """
        with open(self.file_path, encoding="utf-8") as f:
            json_data = json.load(f)
            for item in json_data:
                if (item["title"] == vacancy.title and
                        item["url"] == vacancy.url and
                        item["salary_from"] == vacancy.salary_from and
                        item["salary_to"] == vacancy.salary_to and
                        item["requirements"] == vacancy.requirements and
                        item["responsibility"] == vacancy.responsibility and
                        item["city"] == vacancy.city):
                    json_data.remove(item)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def select_vacancy(self, keyword: str):
        """
        Выбрать вакансии по ключевому слову из файла JSON.

        :param keyword: Ключевое слово для поиска вакансий.
        :return: Список объектов вакансий, соответствующих ключевому слову.
        """
        with open(self.file_path, encoding="utf-8") as f:
            json_data = json.load(f)
            selected_vacancies = []
            for item in json_data:
                if keyword.lower() in item["title"].lower():
                    vacancy = Vacancy(
                        item["title"],
                        item["url"],
                        item["salary_from"],
                        item["salary_to"],
                        item["requirements"],
                        item["responsibility"],
                        item["city"]
                    )
                    selected_vacancies.append(vacancy)
            return selected_vacancies


if __name__ == "__main__":
    hh_api = HHApi()
    hh_vacancies = hh_api.get_vacancies("python разработчик")
    list_vacancies = Vacancy.create_vacancies(hh_vacancies)
    print(list_vacancies)
    for vacancy in list_vacancies:
        print(vacancy)
    print("------------")
    sorted_vacancies = sorted(list_vacancies)
    for vacancy in sorted_vacancies:
        print(f"{vacancy}\n")

    vacancy_1 = Vacancy("Бэкенд-разработчик в Яндекс (Python/Java/C++)", "https://hh.ru/vacancy/99748934", 0, 0,
                        "Опыт коммерческой разработки не менее трёх лет на одном из языков: <highlighttext>Python</highlighttext>, Java, C++.",
                        "", "Россия")

    file_json = JSONWorker("vacancies.json")
    file_json.add_vacancies(list_vacancies)
    file_json.del_vacancy(vacancy_1)
    selected_vacancy = file_json.select_vacancy("Django")
    for vacancy in selected_vacancy:
        print(f"{vacancy}\n")


