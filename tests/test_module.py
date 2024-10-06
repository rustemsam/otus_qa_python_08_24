import requests


def test_url_status_code(url, expected_status_code):
    response = requests.get(url)
    assert (
        response.status_code == expected_status_code
    ), f"Expected status code {expected_status_code}, but got {response.status_code}"
