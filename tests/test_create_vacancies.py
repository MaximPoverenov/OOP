import pytest
def test_create_vacancies():
    vacancies_data = [
        {
            "name": "Python Developer",
            "alternate_url": "http://example.com/python-developer",
            "salary": {"from": 1000, "to": 2000},
            "snippet": {"requirement": "Experience with Django", "responsibility": "Develop web applications"},
            "area": {"name": "New York"}
        },
        {
            "name": "Data Scientist",
            "alternate_url": "http://example.com/data-scientist",
            "salary": None,
            "snippet": {"requirement": "", "responsibility": "Analyze data"},
            "area": {"name": "San Francisco"}
        }
    ]

    vacancies = Vacancy.create_vacancies(vacancies_data)

    assert len(vacancies) == 2

    assert vacancies[0].title == "Python Developer"
    assert vacancies[0].url == "http://example.com/python-developer"
    assert vacancies[0].salary_from == 1000
    assert vacancies[0].salary_to == 2000
    assert vacancies[0].requirements == "Experience with Django"
    assert vacancies[0].responsibility == "Develop web applications"
    assert vacancies[0].city == "New York"

    assert vacancies[1].title == "Data Scientist"
    assert vacancies[1].url == "http://example.com/data-scientist"
    assert vacancies[1].salary_from == 0
    assert vacancies[1].salary_to == 0
    assert vacancies[1].requirements == ""
    assert vacancies[1].responsibility == "Analyze data"
    assert vacancies[1].city == "San Francisco"


if __name__ == "__main__":
    pytest.main()
