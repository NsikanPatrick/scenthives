ENDPOINT = "http://127.0.0.1:8000/api/"

def category_payload():
    payload = {
        "title": "Fiction",
        "gender": "M",
        "slug": "ZixpEXt2tnkj"
    }
    return payload


def create_category(payload):
    return requests.post(ENDPOINT + "categories/", json=payload)


def test_can_create_category():

    payload = category_payload()
    
    create_category_response = create_category(payload)
    assert create_category_response.status_code == 201  

    data = create_category_response.json()

    category_id = data['category_id']
    get_category_response = get_category(category_id)

    assert get_category_response.status_code == 200
    get_category_data = get_category_response.json()