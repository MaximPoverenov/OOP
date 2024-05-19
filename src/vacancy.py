

class Vacancy:
    def __init__(self, title, url, salary, requirements, responsibility, city):
        self.title = title
        self.url = url
        self.salary = salary
        self.requirements = requirements
        self.responsibility = responsibility
        self.city = city
        self.validate()

    def validate(self):
        if not self.salary:
            self.salary_from = 0
            self.salary_to = 0

    @classmethod
    def create_vacancies(cls, vacancies_data):
        instances = []
        for vacancy_info in vacancies_data:
            title = vacancy_info["name"]
            url = vacancy_info["alternate_url"]
            salary = vacancy_info["salary"]
            requirements = vacancy_info["requirement"]
            responsibility = vacancy_info["responsibility"]
            city = vacancy_info["area"]["name"]
            vacancy = cls(title, url, salary, requirements, responsibility, city)
            instances.append(vacancy)
        return instances