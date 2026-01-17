import pytest
from gender_api import Client

@pytest.fixture
def client():
    return Client(api_key="test_key")
