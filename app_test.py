import pytest
from rng_app import app  # Replace with the correct import for your Flask app
from math import ceil
import random
import yaml

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def data():
    with open('racegendernames.yaml', 'r') as file:
        data = yaml.safe_load(file)
        yield data

def test_negative_or_zero_count_redirect(client, data):
    for _ in range(5):  # Perform fuzz testing for half of the data
        response = client.post('/names', data={'count': random.randint(-50, 0), 'ancestry': 'Human', 'gender': 'male'})
        assert response.status_code == 302  # Redirect status code

def test_large_count_redirect(client):
    for _ in range(5):  # Perform fuzz testing for half of the data
        response = client.post('/names', data={'count': random.randint(51, 1000), 'ancestry': 'Elf', 'gender': 'female'})
        assert response.status_code == 302  # Redirect status code

def test_non_int_count_redirect(client):
    response = client.post('/names', data={'count': 'abc', 'ancestry': 'Dwarf', 'gender': 'male'})
    assert response.status_code == 302  # Redirect status code

def test_invalid_ancestry_redirect(client):
    response = client.post('/names', data={'count': 5, 'ancestry': 'Drukhari', 'gender': 'male'})
    assert response.status_code == 302  # Redirect status code

def test_non_bool_gender_redirect(client):
    response = client.post('/names', data={'count': 5, 'ancestry': 'Human', 'gender': 'unknown'})
    assert response.status_code == 302  # Redirect status code

def test_standard_case_length_and_results(client, data):
    for _ in range(ceil(len(data.keys())*0.5)):  # Perform fuzz testing for half of the data
        count = random.randint(5, 50)  # Random count between 5 and 50
        ancestry = random.choice(list(data.keys()))  # Random ancestry from our data
        gender = random.choice(['male', 'female'])  # Random gender
        response = client.post('/names', data={'count': count, 'ancestry': ancestry, 'gender': gender})
        assert response.status_code == 200
