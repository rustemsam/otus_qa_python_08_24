from src.models.gectaro.gectaro_model import (
    ResourceRequestErrorResponse,
    ListResourceRequestPostErrorResponse,
)


class GectaroResponseHelper:
    @staticmethod
    def assert_error_messages(
        response_obj: ResourceRequestErrorResponse,
        expected_error_name: str,
        expected_error_message: str,
        expected_status_code: int,
    ):
        assert (
            expected_error_name == response_obj.name
        ), f"Expected error name '{expected_error_name}', got '{response_obj.name}'"
        assert (
            expected_error_message == response_obj.message
        ), f"Expected error message '{expected_error_message}', got '{response_obj.message}'"
        assert (
            expected_status_code == response_obj.status
        ), f"Expected error code '{expected_status_code}', got '{response_obj.status}'"

    @staticmethod
    def assert_error_messages_for_fields(
        response_obj: ListResourceRequestPostErrorResponse,
        expected_error_messages: list[str],
    ):
        actual_messages = [error.message for error in response_obj.root]

        for expected_message in expected_error_messages:
            assert expected_message in actual_messages, (
                f"Expected error message '{expected_message}' not found in "
                f"actual messages: '{actual_messages}'"
            )
