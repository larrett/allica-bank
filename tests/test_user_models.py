from models.user import UserCreate
import pytest


def test_valid_date_of_birth():
    data = {"first_name": "John", "last_name": "Doe", "date_of_birth": "2000-01-01"}
    user = UserCreate(**data)
    assert user.date_of_birth == "2000-01-01"


def test_invalid_date_of_birth():
    data = {"first_name": "John", "last_name": "Doe", "date_of_birth": "01-01-2000"}
    with pytest.raises(
        ValueError, match="date_of_birth must be in 'YYYY-MM-DD' format"
    ):
        UserCreate(**data)
