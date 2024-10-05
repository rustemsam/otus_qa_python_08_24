import json
import logging
import os
from http import HTTPStatus

import pytest
import requests

from src.helper.gectaro.gectaro_api_helper import GectaroApiHelper
from src.helper.gectaro.gectaro_response_helper import GectaroResponseHelper
from src.helper.response_helper import ResponseHelper
from src.models.gectaro.gectaro_model import (
    ListResourceRequestsResponse,
    ResourceRequestErrorResponse,
    ResourceRequestIdResponse,
    ListResourceRequestPostErrorResponse,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PROJECT_ID = 90719
COMPANY_ID = 7323

DATA_FOR_RESOURCE = {
    "project_tasks_resource_id": "13486869",
    "volume": "1",
    "cost": "100",
    "needed_at": "1720094391",
    "batch_number": "",
    "batch_parent_request_id": "",
    "is_over_budget": "1",
}


@pytest.fixture(scope="session")
def gectaro_api_helper():
    return GectaroApiHelper()


@pytest.fixture(scope="session")
def response_helper():
    return ResponseHelper()


@pytest.fixture(scope="session")
def gectaro_response_helper():
    return GectaroResponseHelper()


@pytest.fixture(scope="session")
def api_key():
    config_path = os.path.join(os.path.dirname(__file__), "../config/config.json")
    api_key = None
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                config = json.load(f)
                api_key = config.get("API_KEY")
        except json.JSONDecodeError:
            logger.error(f"Error parsing {config_path}")
    if not api_key:
        api_key = os.getenv("API_KEY")

    assert api_key, "API Key not found in config.json or environment variables"
    return api_key


@pytest.fixture(scope="session")
def headers(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    logger.info("Using headers: %s", headers)
    return headers


def make_post_request(api_helper, endpoint, headers, data):
    response = requests.post(
        api_helper.post_resource_requests(endpoint), headers=headers, data=data
    )
    return response


@pytest.fixture(scope="session")
def create_resource(headers, gectaro_api_helper, response_helper):
    response = make_post_request(
        gectaro_api_helper, PROJECT_ID, headers, DATA_FOR_RESOURCE
    )
    response_helper.assert_response_status_code(response, HTTPStatus.CREATED)
    post_response = ResourceRequestIdResponse(**response.json())
    return post_response


@pytest.mark.positive
def test_get_resource(headers, gectaro_api_helper, response_helper):
    response = requests.get(
        gectaro_api_helper.get_resource_requests(PROJECT_ID), headers=headers
    )
    response_helper.assert_response_status_code(response)

    expected_length = 20
    list_resource = ListResourceRequestsResponse(response.json())
    assert (
        len(list_resource.root) >= expected_length
    ), f"Expected length is {expected_length}, got {len(list_resource.root)}"


@pytest.mark.negative
@pytest.mark.parametrize(
    "non_existent_project_id",
    [
        10000000,
        #  "*=", TODO Bug #1
        "0",
    ],
)
def test_get_non_existent_project(
    headers,
    non_existent_project_id,
    gectaro_api_helper,
    response_helper,
    gectaro_response_helper,
):
    response = requests.get(
        gectaro_api_helper.get_resource_requests(non_existent_project_id),
        headers=headers,
    )
    response_helper.assert_response_status_code(response, HTTPStatus.NOT_FOUND)

    error_response = ResourceRequestErrorResponse(**response.json())
    gectaro_response_helper.assert_error_messages(
        error_response,
        "Not Found",
        "Выбранный проект недоступен.",
        HTTPStatus.NOT_FOUND,
    )


@pytest.mark.positive
@pytest.mark.parametrize(
    "resource_request",
    [
        # {TODO BUG #2
        #     "project_tasks_resource_id": 13486869,
        #     "volume": 1,
        #     "cost": 100,
        #     "needed_at": "1720094391",
        #     "batch_number": '',
        #     "batch_parent_request_id": 1,
        #     "is_over_budget": 1
        # },
        {
            "project_tasks_resource_id": 13486869,
            "volume": 10,
            "cost": 1,
            "needed_at": "1720094391",
            "batch_number": 1,
            "batch_parent_request_id": "",
            "is_over_budget": 0,
        },
    ],
)
def test_add_resource_request(
    headers,
    gectaro_api_helper,
    response_helper,
    resource_request,
):
    response = requests.post(
        gectaro_api_helper.post_resource_requests(PROJECT_ID),
        headers=headers,
        data=resource_request,
    )

    response_helper.assert_response_status_code(response, HTTPStatus.CREATED)
    post_response = ResourceRequestIdResponse(**response.json())
    response_helper.recursive_compare(post_response, resource_request)


@pytest.mark.negative
@pytest.mark.parametrize(
    "request_data, error_message",
    [
        (
            {
                "project_tasks_resource_id": 0,
                "volume": 0,
                "cost": 100,
                "batch_number": "",
                "batch_parent_request_id": "",
                "is_over_budget": 1,
            },
            "Значение «Ресурс» неверно.",
        ),
        # (
        #     {
        #         'project_tasks_resource_id': 13486869,
        #         'volume': -10,
        #         'cost': -100,
        #         'batch_number': '',
        #         'batch_parent_request_id': '',
        #         'is_over_budget': 0
        #     },
        #     'Значение «Цена» должно быть положительным числом.'
        # ), TODO Bug #4
        (
            {
                "project_tasks_resource_id": 13486869,
                "volume": "l",
                "cost": 1,
                "batch_number": 1,
                "batch_parent_request_id": "",
                "is_over_budget": 0,
            },
            "Значение «Количество» должно быть числом.",
        ),
    ],
)
def test_add_negative_resource_request(
    headers,
    gectaro_api_helper,
    response_helper,
    request_data,
    gectaro_response_helper,
    error_message,
):
    data = {key: f"{value}" for key, value in request_data.items()}

    response = make_post_request(gectaro_api_helper, PROJECT_ID, headers, data)
    response_helper.assert_response_status_code(
        response, HTTPStatus.UNPROCESSABLE_ENTITY
    )

    post_response = ListResourceRequestPostErrorResponse(response.json())
    gectaro_response_helper.assert_error_messages_for_fields(
        post_response, error_message
    )


@pytest.mark.positive
@pytest.mark.ignored  # TODO BUG #5
def test_get_resource_request_id(
    headers, gectaro_api_helper, response_helper, create_resource
):
    post_response = create_resource
    response = requests.get(
        gectaro_api_helper.get_resource_request(PROJECT_ID, post_response.id),
        headers=headers,
    )
    response_helper.assert_response_status_code(response, HTTPStatus.OK)

    get_response = ResourceRequestIdResponse(**response.json())
    response_helper.recursive_compare(get_response, DATA_FOR_RESOURCE)


@pytest.mark.positive
@pytest.mark.parametrize(
    "non_existent_request_id",
    [1, "*=", "1"],
)
def test_get_resource_request_nonexistent_id(
    headers,
    gectaro_api_helper,
    response_helper,
    non_existent_request_id,
    gectaro_response_helper,
):
    response = requests.get(
        gectaro_api_helper.get_resource_request(PROJECT_ID, non_existent_request_id),
        headers=headers,
    )
    response_helper.assert_response_status_code(response, HTTPStatus.NOT_FOUND)

    error_response = ResourceRequestErrorResponse(**response.json())
    gectaro_response_helper.assert_error_messages(
        error_response,
        "Not Found",
        "Запрошенная заявка на ресурс не найдена.",
        HTTPStatus.NOT_FOUND,
    )


@pytest.mark.positive
@pytest.mark.parametrize(
    "request_data",
    [
        (
            {
                "project_tasks_resource_id": 13486869,
                "volume": 1,
                "cost": 100,
                "batch_number": 5,
                "batch_parent_request_id": 100,
                "is_over_budget": 1,
                "created_at": 1720094391,
                "is_deleted": 0,
                "needed_at": 1820094391,
            }
        ),
        (
            {
                "cost": 500,
            }
        ),
        ({"is_deleted": 1, "deleted_at": 1820094391}),
        ({}),
    ],
)
def test_put_resource_request(
    headers, gectaro_api_helper, response_helper, create_resource, request_data
):
    post_response = create_resource
    response = requests.put(
        gectaro_api_helper.put_resource_request(PROJECT_ID, post_response.id),
        headers=headers,
        data=request_data,
    )

    response_helper.assert_response_status_code(response)
    post_response = ResourceRequestIdResponse(**response.json())
    response_helper.recursive_compare(
        post_response,
        request_data,
        ignore_fields=["updated_at", "is_deleted", "deleted_at"],
    )
    # TODO Bug #7
    # TODO Bug #8


@pytest.mark.positive
@pytest.mark.parametrize(
    "request_data, expected_error_messages",
    [
        # TODO BUG #9
        # (
        #
        #     {
        #         'is_deleted': 'deleted',
        #         'deleted_at': 'true'
        #     },
        #     "Invalid is_deleted value"
        # ),
        (
            {"is_over_budget": 2},
            "Значение «сверх бюджета» должно быть равно «1» или «0».",  #
        ),
        (
            {"project_tasks_resource_id": -1, "cost": "invalid"},
            ["Значение «Цена, шт» должно быть числом.", "Значение «Ресурс» неверно."],
        ),
        (
            {"project_tasks_resource_id": "project_tasks_resource_id"},
            "Значение «Ресурс» должно быть целым числом.",
        ),
    ],
)
def test_put_resource_request_negative(
    headers,
    gectaro_api_helper,
    gectaro_response_helper,
    create_resource,
    request_data,
    expected_error_messages,
):
    post_response = create_resource
    response = requests.put(
        gectaro_api_helper.put_resource_request(PROJECT_ID, post_response.id),
        headers=headers,
        data=request_data,
    )

    error_response = ListResourceRequestPostErrorResponse(response.json())
    gectaro_response_helper.assert_error_messages_for_fields(
        error_response, expected_error_messages
    )


@pytest.mark.positive
def test_delete_resource_request(
    headers, gectaro_api_helper, response_helper, create_resource
):
    post_response = create_resource
    response = requests.delete(
        gectaro_api_helper.delete_resource_request(PROJECT_ID, post_response.id),
        headers=headers,
    )
    response_helper.assert_response_status_code(response, HTTPStatus.NO_CONTENT)


@pytest.mark.negative
def test_delete_resource_request_twice(
    headers,
    gectaro_api_helper,
    response_helper,
    gectaro_response_helper,
    create_resource,
):
    post_response = create_resource
    requests.delete(
        gectaro_api_helper.delete_resource_request(PROJECT_ID, post_response.id),
        headers=headers,
    )

    response = requests.delete(
        gectaro_api_helper.delete_resource_request(PROJECT_ID, post_response.id),
        headers=headers,
    )
    error_response = ResourceRequestErrorResponse(**response.json())
    response_helper.assert_response_status_code(response, HTTPStatus.NOT_FOUND)
    gectaro_response_helper.assert_error_messages(
        error_response,
        "Not Found",
        "not_found_project_task_resource",
        HTTPStatus.NOT_FOUND,
    )


@pytest.mark.negative
def test_delete_resource_request_with_wrong_key(
    gectaro_api_helper, response_helper, gectaro_response_helper, create_resource
):
    post_response = create_resource
    headers = {
        "Authorization": "Bearer wrong_api_key",
    }
    response = requests.delete(
        gectaro_api_helper.delete_resource_request(PROJECT_ID, post_response.id),
        headers=headers,
    )
    response_helper.assert_response_status_code(response, HTTPStatus.UNAUTHORIZED)


@pytest.mark.positive
def test_get_company_resource_request(
    headers,
    gectaro_api_helper,
    response_helper,
    gectaro_response_helper,
    create_resource,
):
    response = requests.get(
        gectaro_api_helper.get_company_resource_requests(COMPANY_ID), headers=headers
    )

    response_helper.assert_response_status_code(response)
    list_company_resources = ListResourceRequestsResponse(response.json())
    assert (
        len(list_company_resources.root) >= 1
    ), "Expected at least 1 resource request for the company, but got fewer."


@pytest.mark.negative
@pytest.mark.parametrize(
    "non_existent_company_id",
    [10000000, "0"],
)
def test_get_non_existent_company_resource_request(
    headers,
    non_existent_company_id,
    gectaro_api_helper,
    response_helper,
    gectaro_response_helper,
):
    response = requests.get(
        gectaro_api_helper.get_company_resource_requests(non_existent_company_id),
        headers=headers,
    )
    response_helper.assert_response_status_code(response, HTTPStatus.NOT_FOUND)

    error_response = ResourceRequestErrorResponse(**response.json())

    gectaro_response_helper.assert_error_messages(
        error_response,
        "Not Found",
        "Сущность Company не найдена.",
        HTTPStatus.NOT_FOUND,
    )
