from http import HTTPStatus

import pytest
import requests

from src.helper.dogapi.dog_api_helper import DogApiHelper
from src.helper.response_helper import ResponseHelper
from src.models.dogapi.dog_api_model import (
    DogBreedsApiResponse,
    DogImagesResponse,
    DogBreedListResponse,
    DogRandomImageApiResponse,
)


@pytest.fixture
def dog_api_helper():
    return DogApiHelper()


@pytest.fixture
def response_helper():
    return ResponseHelper()


@pytest.mark.positive
def test_get_random_dog(dog_api_helper, response_helper):
    response = requests.get(dog_api_helper.get_random_dog_image_url())
    response_helper.assert_response_status_code(response)

    dog_api_response = DogRandomImageApiResponse(**response.json())
    expected_message = "https://images.dog.ceo/breeds/"

    response_helper.assert_response_content_type(response)
    assert (
        expected_message in dog_api_response.message
    ), f"The dog image URL does not contain '{expected_message}'"
    response_helper.assert_response_body_status(dog_api_response.status)


@pytest.mark.positive
@pytest.mark.parametrize(
    "expected_breed",
    [
        "bulldog",
        "terrier",
    ],
)
def test_get_list_all_breeds(dog_api_helper, response_helper, expected_breed):
    response = requests.get(dog_api_helper.get_list_all_breeds_url())
    response_helper.assert_response_status_code(response)

    dog_breeds_response = DogBreedsApiResponse(**response.json())
    expected_breed_count = 107

    response_helper.assert_response_content_type(response)
    assert (
        expected_breed in dog_breeds_response.message
    ), f"The breed '{expected_breed}' is not in the response message"
    assert (
        len(dog_breeds_response.message) >= expected_breed_count
    ), f"The expected length is {expected_breed_count}, actual {len(dog_breeds_response.message)}"
    response_helper.assert_response_body_status(dog_breeds_response.status)


@pytest.mark.positive
@pytest.mark.parametrize(
    "breed",
    [
        "akita",
        "sheepdog",
    ],
)
def test_list_images_by_breed(dog_api_helper, response_helper, breed):
    response = requests.get(dog_api_helper.get_list_images_by_breed_url(breed))
    response_helper.assert_response_status_code(response)

    dog_images_response = DogImagesResponse(**response.json())
    expected_message = f"https://images.dog.ceo/breeds/{breed}"

    response_helper.assert_response_content_type(response)
    response_helper.assert_url_contains(dog_images_response.message, expected_message)
    assert len(dog_images_response.message) >= 1, "The expected length is less"
    response_helper.assert_response_body_status(dog_images_response.status)


@pytest.mark.negative
@pytest.mark.parametrize("non_existent_breed", ["dog", "12345", "%"])
def test_list_images_by_non_existent_breed(
    dog_api_helper, response_helper, non_existent_breed
):
    response = requests.get(
        dog_api_helper.get_list_images_by_breed_url(non_existent_breed)
    )
    response_helper.assert_response_status_code(response, HTTPStatus.NOT_FOUND)

    dog_images_response = DogRandomImageApiResponse(**response.json())
    expected_message = "Breed not found (master breed does not exist)"

    response_helper.assert_response_content_type(response)
    assert (
        expected_message in dog_images_response.message
    ), f"Expected message '{expected_message}', got '{dog_images_response.message}'"
    response_helper.assert_response_body_status(dog_images_response.status, "error")


@pytest.mark.positive
@pytest.mark.parametrize(
    "breed, expected_list",
    [
        ("retriever", ["chesapeake", "curly", "flatcoated", "golden"]),
        ("schnauzer", ["giant", "miniature"]),
    ],
)
def test_get_list_all_sub_breeds(dog_api_helper, response_helper, breed, expected_list):
    response = requests.get(dog_api_helper.get_sub_breed_list_url(breed))
    response_helper.assert_response_status_code(response)

    dog_breeds_list_response = DogBreedListResponse(**response.json())

    response_helper.assert_response_content_type(response)
    assert (
        dog_breeds_list_response.message == expected_list
    ), f"The dog breeds URL does not contain '{expected_list}'"
    response_helper.assert_response_body_status(dog_breeds_list_response.status)
