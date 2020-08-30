import pytest
import random
import requests
import math


BASE_URL = "https://dog.ceo/api/"
BREEDS = BASE_URL + "breeds/"
ALL_BREEDS = BREEDS +  "list/all"
BREEDS_IMAGE_RANDOM = BREEDS + "image/random"
BREEDS_IMAGE_RANDOM_MULT = BREEDS + "image/random/{}"
BREED = BASE_URL + 'breed/'
BREED_IMAGE_RANDOM = BREED +"{}/" + "images/random"
BREED_IMAGES = BREED + "{}/" + "images"


def get_random_breeds():
    """
    Вспомогательная функция для отдачи пяти случайных пород.
    """
    response = requests.get(ALL_BREEDS)
    all_breeds = list(response.json()["message"].keys())
    return random.choices(all_breeds, k=5)


def test_random_image_accessibility():
    """
    Проверка доступности случайного изображения
    """
    response = requests.get(BREEDS_IMAGE_RANDOM)
    image_url = response.json()["message"]
    image_response = requests.get(image_url)
    assert response.json()["status"] == "success"
    assert image_response.status_code == 200


@pytest.mark.parametrize("number", [0, 1, 2, 5, 10, 11, 49, 50, 51, 100, 999, 1001, "string", False, 0.01, 3.99, 51.5])
def test_random_image_count(number):
    """
    Проверки, что возвращается запрошенное число изображений.
    Если передаётся дробное число, то дробная часть не учитывается.
    Максимальное возвращаемое число изображений = 50.
    Если передаётся число = 0 или не числовое значение — возвращается 1 изображение.
    """
    response = requests.get(BREEDS_IMAGE_RANDOM_MULT.format(number))
    image_url_list = response.json()["message"]
    if isinstance(number, float):
        number = math.trunc(number)
        if number < 1:
            assert len(image_url_list) == 1
        elif number > 50:
            assert len(image_url_list) == 50
        else:
            assert len(image_url_list) == math.trunc(number)
    elif not isinstance(number, int):
        assert len(image_url_list) == 1
    elif number == 0:
        assert len(image_url_list) == 1
    elif number > 50:
        assert len(image_url_list) == 50
    else:
        assert len(image_url_list) == number

    assert response.json()["status"] == "success"
    assert response.status_code == 200


@pytest.mark.parametrize("breed", get_random_breeds())
def test_random_image_by_breed(breed):
    """
    Проверки, что возвращается случайно изображение запрашиваемой породы.
    """
    response = requests.get(BREED_IMAGE_RANDOM.format(breed))
    image_url = response.json()["message"]
    image_response = requests.get(image_url)
    breed_from_url = image_url.split("/")[-2]
    assert breed_from_url.startswith(breed)
    assert response.json()["status"] == "success"
    assert image_response.status_code == 200


@pytest.mark.parametrize("breed", get_random_breeds())
def test_images_by_breed(breed):
    """
    Проверки, что все возвращаемые изображения относятся к запрашиваемой породе.
    """
    response = requests.get(BREED_IMAGES.format(breed))
    image_url_list = response.json()["message"]
    assert all(breed in image_url for image_url in image_url_list)
    assert response.json()["status"] == "success"
    assert response.status_code == 200


def test_error_for_nonexistent_breed():
    """
    Проверка, что при запросе несуществующей породы возвращается ошибка
    """
    response = requests.get(BREED_IMAGES.format("nonexistent_breed"))
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "Breed not found (master breed does not exist)"
    assert response.json()["code"] == 404
    assert response.status_code == 404
