import unittest
import requests
from app import create_app

URL = "localhost:9090/api/v1.0"

class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TEST")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_valid_post(self):
        r = print(requests.get(URL))
        print(r.text)

    def test_invalid_post(self):
        pass

    def test_valid_get(self):
        pass

    def test_invalid_get(self):
        pass

    def test_valid_put(self):
        pass

    def test_invalid_put(self):
        pass

    def test_get_nearest(self):
        pass

if __name__ == "__main__":
    unittest.main()