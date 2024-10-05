from http import HTTPStatus

import pytest
import requests

from src.helper.brewery.brewery_api_helper import BreweryApiHelper
from src.helper.response_helper import ResponseHelper
from src.models.openbrewerydb.open_brewery_db_model import (
    SingleBreweryResponse,
    ListBreweriesResponse,
    SingleBreweryErrorResponse,
    MetaBreweryResponse,
)


@pytest.fixture
def brewery_api_helper():
    return BreweryApiHelper()


@pytest.fixture
def response_helper():
    return ResponseHelper()


@pytest.mark.positive
@pytest.mark.parametrize(
    "brewer_id",
    [
        "5128df48-79fc-4f0f-8b52-d06be54d0cec",
        "34e8c68b-6146-453f-a4b9-1f6cd99a5ada",
    ],
)
def test_get_single_brewery(brewery_api_helper, response_helper, brewer_id):
    response = requests.get(brewery_api_helper.get_single_brewery(brewer_id))
    response_helper.assert_response_status_code(response)

    single_brewery_response = SingleBreweryResponse(**response.json())
    expected_brewer_type = "micro"
    assert (
        expected_brewer_type in single_brewery_response.brewery_type
    ), f"The brewer type got this {single_brewery_response.brewery_type}, expected this {expected_brewer_type}"


@pytest.mark.positive
def test_get_list_breweries(brewery_api_helper, response_helper):
    response = requests.get(brewery_api_helper.get_list_all_breweries())
    response_helper.assert_response_status_code(response)

    list_breweries_response = ListBreweriesResponse(response.json())

    expected_count_of_breweries = 50
    assert (
        len(list_breweries_response.root) >= expected_count_of_breweries
    ), f"The expected length is {expected_count_of_breweries}, actual {len(list_breweries_response.root)}"


@pytest.mark.positive
def test_get_random_brewery(brewery_api_helper, response_helper):
    response = requests.get(brewery_api_helper.get_random_brewery())
    response_helper.assert_response_status_code(response)

    list_breweries_response = ListBreweriesResponse(response.json())

    expected_length = 1
    assert (
        len(list_breweries_response.root) == expected_length
    ), f"The expected length is {expected_length}, got {len(list_breweries_response.root)} "


@pytest.mark.positive
def test_get_brewery_meta(brewery_api_helper, response_helper):
    response = requests.get(brewery_api_helper.get_brewery_meta())
    response_helper.assert_response_status_code(response)

    meta_brewery_response = MetaBreweryResponse(**response.json())

    expected_page = 1
    expected_per_page = 50
    expected_total = 8323
    assert (
        int(meta_brewery_response.page) == expected_page
    ), f"The expected page is {expected_page}, got {meta_brewery_response.page} "
    assert (
        int(meta_brewery_response.per_page) == expected_per_page
    ), f"The expected  per page is {expected_per_page}, got {meta_brewery_response.per_page} "
    assert (
        int(meta_brewery_response.total) == expected_total
    ), f"The expected total is {expected_total}, got {meta_brewery_response.total} "


@pytest.mark.negative
@pytest.mark.parametrize("non_existent_brewer_id", ["0", "+", "O"])
def test_get_nonexistent_brewery(
    brewery_api_helper, response_helper, non_existent_brewer_id
):
    response = requests.get(
        brewery_api_helper.get_single_brewery(non_existent_brewer_id)
    )
    response_helper.assert_response_status_code(response, HTTPStatus.NOT_FOUND)

    single_brewery_error_response = SingleBreweryErrorResponse(**response.json())
    expected_error_message = "Couldn't find Brewery"
    assert (
        single_brewery_error_response.message == expected_error_message
    ), f"The brewer error message {single_brewery_error_response.message}, expected this {expected_error_message}"
