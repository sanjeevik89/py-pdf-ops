import os
import pytest
from fastapi.testclient import TestClient
from api.pdf_ops import app
from PIL import Image
from io import BytesIO

client = TestClient(app)

def test_decrypt_password_protected_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), '../samples/password_protected_sample.pdf')
    if not os.path.exists(pdf_path):
        pytest.skip('Password-protected sample PDF not found')
    with open(pdf_path, 'rb') as f:
        response = client.post(
            '/decryptPdf',
            files={'file': ('password_protected_sample.pdf', f, 'application/pdf')},
            data={'password': 'test123'}
        )
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/pdf'

def test_decrypt_pdf_wrong_password():
    pdf_path = os.path.join(os.path.dirname(__file__), '../samples/password_protected_sample.pdf')
    if not os.path.exists(pdf_path):
        pytest.skip('Password-protected sample PDF not found')
    with open(pdf_path, 'rb') as f:
        response = client.post(
            '/decryptPdf',
            files={'file': ('password_protected_sample.pdf', f, 'application/pdf')},
            data={'password': 'wrongpass'}
        )
    # Expecting a 400 or 401 error for wrong password
    assert response.status_code in (400, 401)
    assert 'pdf' not in response.headers.get('content-type', '')

def test_decrypt_pdf_no_file():
    response = client.post('/decryptPdf', data={'password': 'test123'})
    assert response.status_code in (400, 422)

def test_compress_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), '../../sample-compress.pdf')
    if not os.path.exists(pdf_path):
        pytest.skip('Sample PDF not found')
    with open(pdf_path, 'rb') as f:
        response = client.post(
            '/compressPdf',
            files={'file': ('sample-compress.pdf', f, 'application/pdf')}
        )
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/pdf'

def test_compress_pdf_no_file():
    response = client.post('/compressPdf')
    assert response.status_code in (400, 422)

def test_images_to_pdf_from_generated_images():
    # Generate a couple of simple images in memory
    img1 = Image.new('RGB', (100, 100), color=(255, 0, 0))
    img2 = Image.new('RGB', (100, 100), color=(0, 255, 0))

    buf1 = BytesIO()
    buf2 = BytesIO()
    img1.save(buf1, format='PNG')
    img2.save(buf2, format='PNG')
    buf1.seek(0)
    buf2.seek(0)

    files = [
        ('files', ('red.png', buf1, 'image/png')),
        ('files', ('green.png', buf2, 'image/png')),
    ]

    response = client.post('/imagesToPdf', files=files)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/pdf'

def test_images_to_pdf_no_files():
    response = client.post('/imagesToPdf')
    assert response.status_code in (400, 422)

