import pytest
from main import app


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_index_page(client):
    """Test if the index page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Incident Data Visualizations' in response.data
