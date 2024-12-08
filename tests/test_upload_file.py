import pytest
import os
from reportlab.pdfgen import canvas
from main import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

@pytest.fixture
def setup_dummy_file():
    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)
    dummy_file_path = os.path.join(upload_folder, 'dummy.pdf')

    # Generate a valid PDF using reportlab
    c = canvas.Canvas(dummy_file_path)
    c.drawString(100, 750, "This is a test PDF.")
    c.save()

    yield dummy_file_path
    os.remove(dummy_file_path)

def test_upload_file(client, setup_dummy_file):
    """Test upload endpoint with a dummy file."""
    dummy_file_path = setup_dummy_file
    with open(dummy_file_path, 'rb') as f:
        response = client.post('/upload', data={'files': (f, 'dummy.pdf')}, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'Files uploaded and processed successfully.' in response.data
