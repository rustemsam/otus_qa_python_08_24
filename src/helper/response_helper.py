from http import HTTPStatus
from typing import List, Union, Any, Dict, Optional

import requests


class ResponseHelper:
    EXPECTED_SUCCESS_STATUS = "success"

    @staticmethod
    def assert_response_content_type(
        response: requests.Response, expected_type="application/json"
    ):
        assert (
            response.headers["Content-Type"] == expected_type
        ), f"Expected content type '{expected_type}', got '{response.headers['Content-Type']}'"

    @staticmethod
    def assert_response_status_code(
        response: requests.Response, expected_status_code=HTTPStatus.OK
    ):
        assert (
            response.status_code == expected_status_code
        ), f"Expected status code '{expected_status_code}', got '{response.status_code}'"

    @staticmethod
    def assert_response_body_status(
        response_status: str, expected_status: str = EXPECTED_SUCCESS_STATUS
    ):
        assert (
            response_status == expected_status
        ), f"Expected status '{expected_status}', got '{response_status}'"

    @staticmethod
    def assert_url_contains(
        urls: List[Union[str, requests.Response]], expected_message: str
    ):
        assert any(
            expected_message in str(url) for url in urls
        ), f"No URL in '{urls}' contains '{expected_message}'"

    @staticmethod
    def recursive_compare(
        response_obj: Any,
        expected_data: Dict[str, Any],
        field_name: Optional[str] = None,
        ignore_fields: Optional[List[str]] = None,
    ):
        if ignore_fields is None:
            ignore_fields = []

        if field_name is None:
            field_name = ""

        for key, expected_value in expected_data.items():
            if key in ignore_fields:
                continue

            response_value = getattr(response_obj, key, None)

            try:
                response_value = int(response_value)
                expected_value = int(expected_value)
            except (ValueError, TypeError):
                pass

            if response_value is None and expected_value == "":
                continue
            elif expected_value is None and response_value == "":
                continue

            assert response_value == expected_value, (
                f"Mismatch in field '{field_name + key}': "
                f"expected {expected_value}, got {response_value}"
            )
