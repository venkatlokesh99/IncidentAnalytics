import pytest
import json
from main import app


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_fetch_no_urls(client):
    """Test fetch endpoint with no URLs provided."""
    response = client.post('/fetch', data=json.dumps({'urls': []}), content_type='application/json')
    assert response.status_code == 400
    assert b'No URLs provided.' in response.data
