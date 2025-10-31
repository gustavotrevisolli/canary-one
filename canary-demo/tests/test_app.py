import unittest
import requests

class TestCanaryApp(unittest.TestCase):
    def setUp(self):
        # Ports in the test environment:
        # - 8080 -> stable service
        # - 8081 -> canary service
        # - 8082 -> ingress controller
        self.stable_url = "http://localhost:8080"
        self.canary_url = "http://localhost:8081"

    def test_homepage_main(self):
        response = requests.get(self.stable_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello from version v1", response.text)
        self.assertIn("background-color: white", response.text)

    def test_homepage_canary(self):
        # Directly hit the canary service port to assert the canary content
        response = requests.get(self.canary_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello from version v2", response.text)
        self.assertIn("background-color: green", response.text)

    def test_metrics(self):
        # Check metrics on the stable instance
        response = requests.get(f"{self.stable_url}/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn("http_requests_total", response.text)

if __name__ == '__main__':
    unittest.main()