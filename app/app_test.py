import pytest
from rng_app import app  # Adjust to the correct import of your Flask app
from math import ceil
import random
import yaml

# Setup Flask test client
@pytest.fixture
def client():
    # Set up the app for testing
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test'

    # Create a test client for making requests
    with app.test_client() as client:
        yield client

# Load test data from the YAML file
@pytest.fixture
def data():
    # Open the YAML file and load the data into the app's config, save to ancestry_generate key 
    with open('names.yaml', 'r') as file:
        data = yaml.safe_load(file)
        app.config['ancestry_generate'] = data
       
       # Yield the loaded data to the tests that use this fixture 
        yield data

# Test redirection for negative or zero count input
def test_negative_or_zero_count_redirect(client, data):
    for _ in range(5): #Perform fuzz testing for half of the data
        response = client.post('/names', data={'count': random.randint(-50, 0), 'ancestry': 'Human', 'gender': 'male'})
        assert response.status_code == 302 # Redirect status code

# Test redirection for overly large count input
def test_large_count_redirect(client):
    for _ in range(5): # Perform fuzz testing for half of the data
        response = client.post('/names', data={'count': random.randint(51, 1000), 'ancestry': 'Elf', 'gender': 'female'})
        assert response.status_code == 302 # Redirect status code

# Test redirection for non-integer count input
def test_non_int_count_redirect(client):
    response = client.post('/names', data={'count': 'abc', 'ancestry': 'Dwarf', 'gender': 'male'})
    assert response.status_code == 302 # Redirect status code

# Test redirection for invalid ancestries
def test_invalid_ancestry_redirect(client):
    response = client.post('/names', data={'count': 5, 'ancestry': 'Drukhari', 'gender': 'male'})
    assert response.status_code == 302 # Redirect status code

# Test redirection for non-binary gender input
def test_non_bool_gender_redirect(client):
    response = client.post('/names', data={'count': 5, 'ancestry': 'Human', 'gender': 'unknown'})
    assert response.status_code == 302 # Redirect status code

# Test successful responses for valid input data
def test_standard_case_length_and_results(client, data):
    for _ in range(ceil(len(data.keys())*0.5)): # Perform fuzz testing for half of the data
        count = random.randint(5, 50) # Random count between 5 and 50
        ancestry = random.choice(list(data.keys())) # Random ancestry from our data
        gender = random.choice(['male', 'female'])  # Random gender
        response = client.post('/names', data={'count': count, 'ancestry': ancestry, 'gender': gender})
        assert response.status_code == 200

