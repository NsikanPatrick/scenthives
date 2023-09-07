import requests
import tempfile
import os
import io
from PIL import Image

ENDPOINT = "http://127.0.0.1:8000/api/"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200



def create_test_image():
    # Create a simple test image using PIL
    width, height = 100, 100
    image = Image.new("RGB", (width, height), "white")
    image_data = io.BytesIO()
    image.save(image_data, format="JPEG")
    image_data.seek(0)
    return image_data

def perfume_payload(image_data):
    payload = {
        "name": "Test Perfume",
        "description": "A test perfume description",
        "price": 50.0,
        "inventory": 100,
        "uploaded_images": [image_data]
    }
    return payload

def create_perfume(payload):
    return requests.post(ENDPOINT + "perfumes/", data=payload, headers={})

def test_can_create_perfume():
    image_data = create_test_image()
    payload = perfume_payload(image_data)

    create_perfume_response = create_perfume(payload)
    assert create_perfume_response.status_code == 201

    data = create_perfume_response.json()

    perfume_id = data['id']
    get_perfume_response = get_perfume(perfume_id)

    assert get_perfume_response.status_code == 200

def get_perfume(perfume_id):
    return requests.get(ENDPOINT + f"perfumes/{perfume_id}/")
