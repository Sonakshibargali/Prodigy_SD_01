"""
Unit tests for Flask application routes and API endpoints.
"""

import unittest
from app import app


class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes and API responses."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_page_get(self):
        """Test home page loads with 200 OK and expected form elements."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        content = response.data.decode("utf-8")
        self.assertIn("Temperature Converter", content)

    def test_api_convert_success_celsius(self):
        """Test API endpoint converting 100 Celsius."""
        response = self.client.post(
            "/api/convert",
            json={"temperature": 100, "unit": "C"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        results = data["data"]["results"]
        self.assertEqual(len(results), 2)
        
        # Verify Fahrenheit result is 212.00
        f_res = next(r for r in results if r["unit"] == "F")
        self.assertEqual(f_res["formatted"], "212.00")
        
        # Verify Kelvin result is 373.15
        k_res = next(r for r in results if r["unit"] == "K")
        self.assertEqual(k_res["formatted"], "373.15")

    def test_api_convert_success_fahrenheit(self):
        """Test API endpoint converting 32 Fahrenheit."""
        response = self.client.post(
            "/api/convert",
            json={"temperature": "32", "unit": "F"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        results = data["data"]["results"]
        
        c_res = next(r for r in results if r["unit"] == "C")
        self.assertEqual(c_res["formatted"], "0.00")

    def test_api_convert_success_kelvin(self):
        """Test API endpoint converting 0 Kelvin (absolute zero)."""
        response = self.client.post(
            "/api/convert",
            json={"temperature": 0, "unit": "K"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        results = data["data"]["results"]
        
        c_res = next(r for r in results if r["unit"] == "C")
        self.assertEqual(c_res["formatted"], "-273.15")

    def test_api_convert_empty_input(self):
        """Test API endpoint with empty input string."""
        response = self.client.post(
            "/api/convert",
            json={"temperature": "   ", "unit": "C"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("cannot be empty", data["error"])

    def test_api_convert_non_numeric_input(self):
        """Test API endpoint with non-numeric value."""
        response = self.client.post(
            "/api/convert",
            json={"temperature": "invalid_num", "unit": "C"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("valid number", data["error"])

    def test_api_convert_kelvin_below_zero(self):
        """Test API endpoint rejecting Kelvin below 0."""
        response = self.client.post(
            "/api/convert",
            json={"temperature": -5, "unit": "K"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("cannot be below absolute zero", data["error"])

    def test_api_convert_missing_fields(self):
        """Test API endpoint missing fields."""
        response = self.client.post(
            "/api/convert",
            json={"temperature": 100}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])

    def test_form_submission_success(self):
        """Test HTML form POST submission returns 200 and displays converted results."""
        response = self.client.post(
            "/",
            data={"temperature": "25", "unit": "C"}
        )
        self.assertEqual(response.status_code, 200)
        content = response.data.decode("utf-8")
        self.assertIn("77.00", content)
        self.assertIn("298.15", content)

    def test_form_submission_validation_error(self):
        """Test HTML form POST submission with invalid input shows error."""
        response = self.client.post(
            "/",
            data={"temperature": "-10", "unit": "K"}
        )
        self.assertEqual(response.status_code, 200)
        content = response.data.decode("utf-8")
        self.assertIn("cannot be below absolute zero", content)


if __name__ == "__main__":
    unittest.main()
