from typing import List
from src.api import HHApi
class Vacancy:
    """
    Класс для представления вакансии.

    Attributes:
        title (str): Название вакансии.
        url (str): URL вакансии.
        salary_from (int): Минимальная зарплата.
        salary_to (int): Максимальная зарплата.
        requirements (str): Требования к кандидату.
        responsibility (str): Обязанности на должности.
        city (str): Город, в котором расположена вакансия.
    """
    def __init__(self, title: str, url: str, salary_from: int, salary_to: int, requirements: str, responsibility: str, city: str) -> None:
        """
        Инициализация объекта Vacancy.

        :param title: Название вакансии.
        :param url: URL вакансии.
        :param salary_from: Минимальная зарплата.
        :param salary_to: Максимальная зарплата.
        :param requirements: Требования к кандидату.
        :param responsibility: Обязанности на должности.
        :param city: Город, в котором расположена вакансия.
        """
        self.title: str = title
        self.url: str = url
        self.salary_from: int = salary_from if salary_from else 0
        self.salary_to: int = salary_to if salary_to else 0
        self.requirements: str = requirements if requirements else ""
        self.responsibility: str = responsibility if responsibility else ""
        self.city: str = city

    @classmethod
    def create_vacancies(cls, vacancies_data: List[dict]) -> List['Vacancy']:
        """
        Создает список объектов Vacancy на основе данных о вакансиях.

        :param vacancies_data: Список словарей с данными о вакансиях.
        :return: Список объектов Vacancy.
        """
        instances: List['Vacancy'] = []
        for vacancy_info in vacancies_data:
            title: str = vacancy_info["name"]
            url: str = vacancy_info["alternate_url"]

            salary = vacancy_info.get("salary")
            salary_from: int = salary.get("from") if salary else 0
            salary_to: int = salary.get("to") if salary else 0

            requirements: str = vacancy_info["snippet"].get("requirement", "")
            responsibility: str = vacancy_info["snippet"].get("responsibility", "")
            city: str = vacancy_info["area"]["name"]

            vacancy: 'Vacancy' = cls(title, url, salary_from, salary_to, requirements, responsibility, city)
            instances.append(vacancy)
        return instances

    def __lt__(self, other: 'Vacancy') -> bool:
        """
        Сравнивает вакансии по минимальной зарплате для сортировки.

        :param other: Другой объект Vacancy для сравнения.
        :return: True, если минимальная зарплата текущей вакансии больше, чем у другой вакансии.
        """
        return self.salary_from > other.salary_from

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта Vacancy.

        :return: Строка с информацией о вакансии.
        """
        return (f"Профессия: {self.title}\n"
                f"Ссылка: {self.url}\n"
                f"Зарплата: от {self.salary_from} до {self.salary_to}\n"
                f"Требования: {self.requirements}\n"
                f"Ответственность: {self.responsibility}\n"
                f"Город: {self.city}")

if __name__ == "__main__":
    hh_api: HHApi = HHApi()
    hh_vacancies: List[dict] = hh_api.get_vacancies("python developer")
    list_vacancies: List[Vacancy] = Vacancy.create_vacancies(hh_vacancies)
    print(list_vacancies)
    for vacancy in list_vacancies:
        print(vacancy)
    print('____________________________________________________________________\n')
    sorted_vacancies: List[Vacancy] = sorted(list_vacancies)
    for vacancy in sorted_vacancies:
        print(vacancy)

    vacancy1: Vacancy = Vacancy('python', "hh.ru", 50000, 60000, '', '', "")
    vacancy2: Vacancy = Vacancy('developer', "hh.ru", 61000, 70000, 'Опыт python', "Писать код", 'Калининград')
    print(vacancy1)
    print(vacancy2)
    print(vacancy1 == vacancy2)
    print(vacancy1 < vacancy2)
    print(vacancy1 > vacancy2)
