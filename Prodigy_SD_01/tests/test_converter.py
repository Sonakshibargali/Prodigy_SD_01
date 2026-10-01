"""
Unit tests for the temperature converter module.
"""

import unittest
from converter import (
    convert_temperature,
    validate_temperature,
    celsius_to_fahrenheit,
    celsius_to_kelvin,
    fahrenheit_to_celsius,
    fahrenheit_to_kelvin,
    kelvin_to_celsius,
    kelvin_to_fahrenheit,
    TemperatureConversionError,
    ABSOLUTE_ZERO_CELSIUS,
    ABSOLUTE_ZERO_FAHRENHEIT,
    ABSOLUTE_ZERO_KELVIN,
)


class TestConverterFormulas(unittest.TestCase):
    """Test standard conversion formulas directly."""

    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0), 32.0, places=2)
        self.assertAlmostEqual(celsius_to_fahrenheit(100), 212.0, places=2)
        self.assertAlmostEqual(celsius_to_fahrenheit(-40), -40.0, places=2)
        self.assertAlmostEqual(celsius_to_fahrenheit(37), 98.6, places=2)

    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(celsius_to_kelvin(0), 273.15, places=2)
        self.assertAlmostEqual(celsius_to_kelvin(100), 373.15, places=2)
        self.assertAlmostEqual(celsius_to_kelvin(-273.15), 0.0, places=2)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(fahrenheit_to_celsius(32), 0.0, places=2)
        self.assertAlmostEqual(fahrenheit_to_celsius(212), 100.0, places=2)
        self.assertAlmostEqual(fahrenheit_to_celsius(-40), -40.0, places=2)
        self.assertAlmostEqual(fahrenheit_to_celsius(98.6), 37.0, places=2)

    def test_fahrenheit_to_kelvin(self):
        self.assertAlmostEqual(fahrenheit_to_kelvin(32), 273.15, places=2)
        self.assertAlmostEqual(fahrenheit_to_kelvin(212), 373.15, places=2)
        self.assertAlmostEqual(fahrenheit_to_kelvin(-459.67), 0.0, places=2)

    def test_kelvin_to_celsius(self):
        self.assertAlmostEqual(kelvin_to_celsius(273.15), 0.0, places=2)
        self.assertAlmostEqual(kelvin_to_celsius(373.15), 100.0, places=2)
        self.assertAlmostEqual(kelvin_to_celsius(0), -273.15, places=2)

    def test_kelvin_to_fahrenheit(self):
        self.assertAlmostEqual(kelvin_to_fahrenheit(273.15), 32.0, places=2)
        self.assertAlmostEqual(kelvin_to_fahrenheit(373.15), 212.0, places=2)
        self.assertAlmostEqual(kelvin_to_fahrenheit(0), -459.67, places=2)


class TestValidation(unittest.TestCase):
    """Test inputs and absolute zero boundary validations."""

    def test_empty_input(self):
        with self.assertRaises(TemperatureConversionError) as ctx:
            validate_temperature("", "C")
        self.assertIn("cannot be empty", str(ctx.exception))

        with self.assertRaises(TemperatureConversionError) as ctx:
            validate_temperature(None, "C")
        self.assertIn("cannot be empty", str(ctx.exception))

    def test_non_numeric_input(self):
        with self.assertRaises(TemperatureConversionError) as ctx:
            validate_temperature("abc", "C")
        self.assertIn("valid number", str(ctx.exception))

        with self.assertRaises(TemperatureConversionError) as ctx:
            validate_temperature("25a", "C")
        self.assertIn("valid number", str(ctx.exception))

    def test_invalid_unit(self):
        with self.assertRaises(TemperatureConversionError) as ctx:
            validate_temperature(100, "X")
        self.assertIn("Invalid unit", str(ctx.exception))

    def test_kelvin_below_zero(self):
        with self.assertRaises(TemperatureConversionError) as ctx:
            validate_temperature(-0.01, "K")
        self.assertIn("below absolute zero", str(ctx.exception))

        with self.assertRaises(TemperatureConversionError) as ctx:
            validate_temperature(-50, "K")
        self.assertIn("below absolute zero", str(ctx.exception))

    def test_celsius_below_absolute_zero(self):
        with self.assertRaises(TemperatureConversionError) as ctx:
            validate_temperature(-273.16, "C")
        self.assertIn("below absolute zero", str(ctx.exception))

    def test_fahrenheit_below_absolute_zero(self):
        with self.assertRaises(TemperatureConversionError) as ctx:
            validate_temperature(-459.68, "F")
        self.assertIn("below absolute zero", str(ctx.exception))

    def test_absolute_zero_exact_boundary_valid(self):
        # Boundaries must pass validation
        self.assertEqual(validate_temperature(ABSOLUTE_ZERO_KELVIN, "K"), 0.0)
        self.assertEqual(validate_temperature(ABSOLUTE_ZERO_CELSIUS, "C"), -273.15)
        self.assertEqual(validate_temperature(ABSOLUTE_ZERO_FAHRENHEIT, "F"), -459.67)


class TestConvertTemperature(unittest.TestCase):
    """Test full conversion workflow and output structure."""

    def test_convert_celsius_normal(self):
        data = convert_temperature(25, "C")
        self.assertEqual(data["input"]["formatted"], "25.00")
        self.assertEqual(data["input"]["unit"], "C")
        self.assertEqual(len(data["results"]), 2)

        # Result 1: Fahrenheit (77.00)
        f_result = next(r for r in data["results"] if r["unit"] == "F")
        self.assertEqual(f_result["formatted"], "77.00")
        self.assertEqual(f_result["symbol"], "°F")

        # Result 2: Kelvin (298.15)
        k_result = next(r for r in data["results"] if r["unit"] == "K")
        self.assertEqual(k_result["formatted"], "298.15")
        self.assertEqual(k_result["symbol"], "K")

    def test_convert_fahrenheit_normal(self):
        data = convert_temperature(68, "F")
        self.assertEqual(data["input"]["formatted"], "68.00")
        self.assertEqual(data["input"]["unit"], "F")

        # Result 1: Celsius (20.00)
        c_result = next(r for r in data["results"] if r["unit"] == "C")
        self.assertEqual(c_result["formatted"], "20.00")

        # Result 2: Kelvin (293.15)
        k_result = next(r for r in data["results"] if r["unit"] == "K")
        self.assertEqual(k_result["formatted"], "293.15")

    def test_convert_kelvin_normal(self):
        data = convert_temperature(300, "K")
        self.assertEqual(data["input"]["formatted"], "300.00")
        self.assertEqual(data["input"]["unit"], "K")

        # Result 1: Celsius (26.85)
        c_result = next(r for r in data["results"] if r["unit"] == "C")
        self.assertEqual(c_result["formatted"], "26.85")

        # Result 2: Fahrenheit (80.33)
        f_result = next(r for r in data["results"] if r["unit"] == "F")
        self.assertEqual(f_result["formatted"], "80.33")

    def test_convert_string_input_valid(self):
        data = convert_temperature(" 100.5 ", "c")
        self.assertEqual(data["input"]["formatted"], "100.50")
        self.assertEqual(data["input"]["unit"], "C")


if __name__ == "__main__":
    unittest.main()
