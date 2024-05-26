from src.vacancy import Vacancy
from src.api import HHApi
from src.worker import JSONWorker


def user_interaction():
    """
    Взаимодействие с пользователем для поиска и фильтрации вакансий.

    Функция запрашивает у пользователя параметры поиска, получает вакансии с использованием API,
    сохраняет их в файл JSON, фильтрует по ключевым словам и зарплате, а затем выводит отфильтрованные вакансии.

    Шаги выполнения:
    1. Запрос поискового запроса у пользователя.
    2. Запрос количества вакансий для отображения (топ N).
    3. Запрос ключевых слов для фильтрации.
    4. Запрос желаемой зарплаты.
    5. Получение вакансий с использованием API.
    6. Сохранение вакансий в файл JSON.
    7. Фильтрация вакансий по ключевым словам.
    8. Фильтрация вакансий по желаемой зарплате.
    9. Сортировка и вывод отфильтрованных вакансий.

    """
    api_hh = HHApi()
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    desired_salary = int(input("Введите желаемую зарплату: "))

    vacancies_info = api_hh.get_vacancies(search_query.lower())
    vacancies = Vacancy.create_vacancies(vacancies_info)

    file_worker = JSONWorker("vacancies.json")
    file_worker.add_vacancies(vacancies)

    selected_vacancies = set()
    if not filter_words:
        selected_vacancies.update(set(file_worker.return_list_vacancies()))
    else:
        for word in filter_words:
            list_vacancies = set(file_worker.select_vacancy(word))
            selected_vacancies.update(list_vacancies)

    ready_vacancies = [vacancy for vacancy in selected_vacancies if desired_salary <= vacancy.salary_from]
    result = sorted(ready_vacancies)

    for item in result[0:top_n]:
        print(item, '\n')
