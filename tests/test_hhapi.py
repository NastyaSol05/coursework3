from typing import Any
from unittest.mock import Mock, patch

from src.hhapi import HhAPI


@patch("requests.get")
def test_get_vacancies_with_query(mock_get: Any) -> None:
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {"name": "Python Developer", "url": "https://example.com/vacancy/1"},
            {"name": "Java Developer", "url": "https://example.com/vacancy/2"},
        ]
    }

    mock_get.return_value = mock_response

    api = HhAPI()
    vacancies = api.get_vacancies(query="Python")

    mock_get.assert_called_once_with(url=api.url, params={"text": "Python", "page": 0, "per_page": 100})
    assert len(vacancies) == 2
    assert vacancies[0]["name"] == "Python Developer"
    assert vacancies[1]["name"] == "Java Developer"
