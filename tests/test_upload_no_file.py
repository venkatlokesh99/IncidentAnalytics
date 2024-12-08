import pytest
from main import app


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_upload_no_file(client):
    """Test upload endpoint with no file provided."""
    response = client.post('/upload', data={})
    assert response.status_code == 400
    assert b'No files provided.' in response.data
