import pytest
from main import app


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_visualize_empty_data(client):
    """Test visualize endpoint when no data is available."""
    response = client.get('/visualize')
    assert response.status_code == 400
    assert b'No data available for visualization.' in response.data
