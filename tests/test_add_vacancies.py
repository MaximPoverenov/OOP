import pytest
import json
import os
from unittest import mock
from src.worker import JSONWorker  # Предполагается, что ваш код находится в файле worker.py
from src.vacancy import Vacancy

DATA_PATH = "test_data"


def setup_module(module):
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)


def teardown_module(module):
    for filename in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    os.rmdir(DATA_PATH)


def test_add_vacancies():
    file_name = "vacancies.json"
    worker = JSONWorker(file_name)

    vacancies = [
        Vacancy("Python Developer", "http://example.com/python-developer", 1000, 2000, "Experience with Django",
                "Develop web applications", "New York"),
        Vacancy("Data Scientist", "http://example.com/data-scientist", 0, 0, "", "Analyze data", "San Francisco")
    ]

    worker.add_vacancies(vacancies)

    with open(worker.file_path, encoding="utf-8") as f:
        json_data = json.load(f)

    assert len(json_data) == 2
    assert json_data[0]["title"] == "Python Developer"
    assert json_data[0]["url"] == "http://example.com/python-developer"
    assert json_data[0]["salary_from"] == 1000
    assert json_data[0]["salary_to"] == 2000
    assert json_data[0]["requirements"] == "Experience with Django"
    assert json_data[0]["responsibility"] == "Develop web applications"
    assert json_data[0]["city"] == "New York"

    assert json_data[1]["title"] == "Data Scientist"
    assert json_data[1]["url"] == "http://example.com/data-scientist"
    assert json_data[1]["salary_from"] == 0
    assert json_data[1]["salary_to"] == 0
    assert json_data[1]["requirements"] == ""
    assert json_data[1]["responsibility"] == "Analyze data"
    assert json_data[1]["city"] == "San Francisco"


def test_file_creation():
    file_name = "new_vacancies.json"
    worker = JSONWorker(file_name)

    assert os.path.exists(worker.file_path)
    with open(worker.file_path, encoding="utf-8") as f:
        json_data = json.load(f)
    assert json_data == []


def test_add_vacancies_to_existing_file():
    file_name = "existing_vacancies.json"
    worker = JSONWorker(file_name)

    initial_vacancies = [
        Vacancy("Frontend Developer", "http://example.com/frontend-developer", 500, 1500, "Experience with React",
                "Develop UI components", "Chicago")
    ]

    worker.add_vacancies(initial_vacancies)

    new_vacancies = [
        Vacancy("Backend Developer", "http://example.com/backend-developer", 1200, 2500, "Experience with Node.js",
                "Develop backend services", "Los Angeles")
    ]

    worker.add_vacancies(new_vacancies)

    with open(worker.file_path, encoding="utf-8") as f:
        json_data = json.load(f)

    assert len(json_data) == 2
    assert json_data[0]["title"] == "Frontend Developer"
    assert json_data[0]["url"] == "http://example.com/frontend-developer"
    assert json_data[0]["salary_from"] == 500
    assert json_data[0]["salary_to"] == 1500
    assert json_data[0]["requirements"] == "Experience with React"
    assert json_data[0]["responsibility"] == "Develop UI components"
    assert json_data[0]["city"] == "Chicago"

    assert json_data[1]["title"] == "Backend Developer"
    assert json_data[1]["url"] == "http://example.com/backend-developer"
    assert json_data[1]["salary_from"] == 1200
    assert json_data[1]["salary_to"] == 2500
    assert json_data[1]["requirements"] == "Experience with Node.js"
    assert json_data[1]["responsibility"] == "Develop backend services"
    assert json_data[1]["city"] == "Los Angeles"


if __name__ == "__main__":
    pytest.main()
