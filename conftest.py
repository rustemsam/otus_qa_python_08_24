from http import HTTPStatus

import pytest


def pytest_addoption(parser):
    print("Adding command line options...")
    parser.addoption("--url", default="https://ya.ru", help="URL to test")
    parser.addoption(
        "--status-code",
        default=str(HTTPStatus.OK.value),
        type=int,
        help="Expected status code",
    )


@pytest.fixture
def url(request) -> str:
    return request.config.getoption("--url")


@pytest.fixture
def expected_status_code(request) -> int:
    return request.config.getoption("--status-code")
