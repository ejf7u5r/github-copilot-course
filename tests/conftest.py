import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

_initial_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(_initial_activities))


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
