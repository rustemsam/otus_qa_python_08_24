from http import HTTPStatus

import pytest
import requests

from src.helper.jsonplaceholder.jsonplaceholder_api_helper import (
    JsonPlaceholderApiHelper,
)
from src.helper.response_helper import ResponseHelper
from src.models.jsonplaceholder.jsonplaceholder_model import (
    PostsRequestBody,
    PostsResponseBody,
    ListPostsResponse,
)

post_request = PostsRequestBody(title="Otus1", body="otus course", userId=1)


@pytest.fixture(scope="session")
def jsonplaceholder_api_helper():
    return JsonPlaceholderApiHelper()


@pytest.fixture(scope="session")
def response_helper():
    return ResponseHelper()


@pytest.fixture(scope="session")
def create_post(jsonplaceholder_api_helper, response_helper):
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        jsonplaceholder_api_helper.create_post(),
        data=post_request.model_dump_json(),
        headers=headers,
    )
    post_response = PostsResponseBody(**response.json())
    response_helper.assert_response_status_code(response, HTTPStatus.CREATED)
    return post_response


@pytest.mark.positive
def test_create_post(response_helper, create_post):
    post_response = create_post

    assert (
        post_response.body == post_request.body
    ), f"The expected body {post_request.body}, got {post_response.body}"
    assert (
        post_response.title == post_request.title
    ), f"The expected title {post_request.title}, got {post_response.title}"
    assert (
        post_response.userId == post_request.userId
    ), f"The expected user id {post_request.userId}, got {post_response.userId}"


@pytest.mark.positive
def test_update_post(jsonplaceholder_api_helper, response_helper):
    headers = {"Content-Type": "application/json"}
    post_id = 10
    response = requests.put(
        jsonplaceholder_api_helper.update_post(post_id),
        data=post_request.model_dump_json(),
        headers=headers,
    )

    response_helper.assert_response_status_code(response)
    put_response = PostsResponseBody(**response.json())

    assert (
        put_response.body == post_request.body
    ), f"The expected body {post_request.body}, got {put_response.body}"
    assert (
        put_response.title == post_request.title
    ), f"The expected title {post_request.title}, got {put_response.title}"
    assert (
        put_response.userId == post_request.userId
    ), f"The expected user id {post_request.userId}, got {put_response.userId}"


@pytest.mark.positive
@pytest.mark.parametrize(
    "post_id",
    [1, 100],
)
def test_get_post(jsonplaceholder_api_helper, response_helper, post_id):
    response = requests.get(jsonplaceholder_api_helper.get_post(post_id))
    response_helper.assert_response_status_code(response)

    get_response = PostsResponseBody(**response.json())

    assert (
        get_response.id == post_id
    ), f"Expected post ID to be {post_id}, but got {get_response.id}"
    assert (
        get_response.title is not None
    ), "Expected title to be present in the response"
    assert get_response.body is not None, "Expected body to be present in the response"
    assert (
        get_response.userId is not None
    ), "Expected userId to be present in the response"


@pytest.mark.positive
def test_get_all_posts(jsonplaceholder_api_helper, response_helper):
    response = requests.get(jsonplaceholder_api_helper.get_list_all_posts())
    response_helper.assert_response_status_code(response)

    get_response = ListPostsResponse(response.json())
    expected_number_of_posts = 100
    assert (
        len(get_response.root) == expected_number_of_posts
    ), f"The expected length is {expected_number_of_posts}, got {len(get_response.root)} "


@pytest.mark.negative
@pytest.mark.parametrize(
    "post_id",
    [101, "otus", "!"],
)
def test_get_nonexistent_post(jsonplaceholder_api_helper, response_helper, post_id):
    response = requests.get(jsonplaceholder_api_helper.get_post(post_id))
    response_helper.assert_response_status_code(response, HTTPStatus.NOT_FOUND)
