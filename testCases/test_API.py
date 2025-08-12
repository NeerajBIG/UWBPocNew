import requests
import json

# Define the API endpoint
BASE_URL = "https://jsonplaceholder.typicode.com" # Example public API

def test_get_posts():
    """
    PoC for a GET request and basic response validation.
    """
    endpoint = f"{BASE_URL}/posts/1"
    response = requests.get(endpoint)

    # Assertions
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, dict), "Response should be a dictionary"
    assert "userId" in data, "Response should contain 'userId'"
    assert data["id"] == 1, "Incorrect post ID"
    print(f"GET request successful for {endpoint}")
    print(f"Response data: {json.dumps(data, indent=2)}")

def test_create_post():
    """
    PoC for a POST request and response validation.
    """
    endpoint = f"{BASE_URL}/posts"
    new_post = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(endpoint, json=new_post, headers=headers)

    # Assertions
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    data = response.json()
    assert isinstance(data, dict), "Response should be a dictionary"
    assert "id" in data, "Response should contain 'id'"
    assert data["title"] == "foo", "Incorrect title in created post"
    print(f"POST request successful for {endpoint}")
    print(f"Response data: {json.dumps(data, indent=2)}")

if __name__ == "__main__":
    print("Running API Testing PoC...")
    test_get_posts()
    print("-" * 30)
    test_create_post()
    print("\nAPI Testing PoC completed.")