import allure
import pytest
import requests
import jsonschema
from .schemas import *

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }

            response = requests.put(f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_pet_full(self):
        with allure.step("Подготовка данных для создания питомца c полными данными"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category":
                    {
                        "id": 1,
                        "name": "Dogs"
                    },
                "photoUrls": ["string"],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца c полными данными"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "категория питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "фото питомца не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "тег питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response_create_pet = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response_create_pet.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response_create_pet.json()["id"] == pet_id

        with allure.step("Отправка запроса на обновление существующего питомца"):
            payload_update_pet = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

            response_update_pet = requests.put(f"{BASE_URL}/pet", json=payload_update_pet)
            response_update_pet_json = response_update_pet.json()

        with allure.step("Проверка статуса ответа"):
            assert response_update_pet.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка обновлённых параметров питомца в ответе"):
            assert response_update_pet_json['id'] == payload_update_pet['id'], "ID питомца не совпадает с ожидаемым"
            assert response_update_pet_json['name'] == payload_update_pet['name'], "имя питомца не совпадает с ожидаемым"
            assert response_update_pet_json['status'] == payload_update_pet['status'], "статус питомца не совпадает с ожидаемым"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response_create_pet = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response_create_pet.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response_create_pet.json()["id"] == pet_id

        with allure.step("Отправка запроса на удаление существующего питомца"):
            response_delete_pet = requests.delete(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response_delete_pet.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации о несуществующем питомце по ID"):
            response_get_nonexistent_pet = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response_get_nonexistent_pet.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение списка питомцев по статусам разрешённого списка")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200),
        ]
    )
    def test_get_pet_by_status_allowed(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение информации питомцев по статусу {status}"):
            test_get_pet_by_status_allowed = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа и формат данных"):
            assert test_get_pet_by_status_allowed.status_code == expected_status_code, "Код ответа не совпал с ожидаемым"
            assert isinstance(test_get_pet_by_status_allowed.json(), list)

    @allure.title("Получение списка питомцев по статусам запрещённого списка")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("nonexistent", 400),
            ("", 400),
        ]
    )
    def test_get_pet_by_status_forbidden(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение информации питомцев по статусу {status}"):
            test_get_pet_by_status_forbidden = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа"):
            assert test_get_pet_by_status_forbidden.status_code == expected_status_code, "Код ответа не совпал с ожидаемым"