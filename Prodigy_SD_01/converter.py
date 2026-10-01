"""
Temperature Converter Module
Contains the core business logic for converting temperatures between
Celsius, Fahrenheit, and Kelvin with absolute zero validation.
"""

from typing import Dict, Any

# Absolute zero constants for validation
ABSOLUTE_ZERO_CELSIUS = -273.15
ABSOLUTE_ZERO_FAHRENHEIT = -459.67
ABSOLUTE_ZERO_KELVIN = 0.0

UNIT_LABELS = {
    "C": {"name": "Celsius", "symbol": "°C"},
    "F": {"name": "Fahrenheit", "symbol": "°F"},
    "K": {"name": "Kelvin", "symbol": "K"},
}


class TemperatureConversionError(ValueError):
    """Custom exception raised when temperature conversion fails validation."""
    pass


def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (c * 9.0 / 5.0) + 32.0


def celsius_to_kelvin(c: float) -> float:
    """Convert Celsius to Kelvin."""
    return c + 273.15


def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (f - 32.0) * 5.0 / 9.0


def fahrenheit_to_kelvin(f: float) -> float:
    """Convert Fahrenheit to Kelvin."""
    return (f - 32.0) * 5.0 / 9.0 + 273.15


def kelvin_to_celsius(k: float) -> float:
    """Convert Kelvin to Celsius."""
    return k - 273.15


def kelvin_to_fahrenheit(k: float) -> float:
    """Convert Kelvin to Fahrenheit."""
    return (k - 273.15) * 9.0 / 5.0 + 32.0


def validate_temperature(value: Any, unit: str) -> float:
    """
    Validates that the input value is numeric and does not fall below absolute zero.

    Args:
        value: Numeric or string representation of a number.
        unit: 'C', 'F', or 'K' (case-insensitive).

    Returns:
        float: Validated temperature value.

    Raises:
        TemperatureConversionError: If input is empty, non-numeric, or below absolute zero.
    """
    if value is None or (isinstance(value, str) and value.strip() == ""):
        raise TemperatureConversionError("Temperature value cannot be empty.")

    try:
        numeric_value = float(value)
    except (ValueError, TypeError):
        raise TemperatureConversionError(f"Invalid temperature '{value}'. Please enter a valid number.")

    normalized_unit = str(unit).strip().upper()
    if normalized_unit not in UNIT_LABELS:
        raise TemperatureConversionError(f"Invalid unit '{unit}'. Supported units are: C, F, K.")

    # Validate against absolute zero
    if normalized_unit == "K" and numeric_value < ABSOLUTE_ZERO_KELVIN:
        raise TemperatureConversionError("Temperature cannot be below absolute zero (0.00 K).")
    elif normalized_unit == "C" and numeric_value < ABSOLUTE_ZERO_CELSIUS:
        raise TemperatureConversionError("Temperature cannot be below absolute zero (-273.15 °C).")
    elif normalized_unit == "F" and numeric_value < ABSOLUTE_ZERO_FAHRENHEIT:
        raise TemperatureConversionError("Temperature cannot be below absolute zero (-459.67 °F).")

    return numeric_value


def convert_temperature(value: Any, unit: str) -> Dict[str, Any]:
    """
    Converts a temperature from the provided unit to the other two units.

    Args:
        value: The temperature value (float or string representation).
        unit: The source unit ('C', 'F', or 'K').

    Returns:
        A dictionary containing input metadata and the two converted values formatted to 2 decimal places:
        {
            "input": {"value": 25.0, "formatted": "25.00", "unit": "C", "symbol": "°C", "name": "Celsius"},
            "results": [
                {"unit": "F", "name": "Fahrenheit", "symbol": "°F", "value": 77.0, "formatted": "77.00"},
                {"unit": "K", "name": "Kelvin", "symbol": "K", "value": 298.15, "formatted": "298.15"}
            ]
        }
    """
    normalized_unit = str(unit).strip().upper()
    temp = validate_temperature(value, normalized_unit)

    results = []

    if normalized_unit == "C":
        f_val = celsius_to_fahrenheit(temp)
        k_val = celsius_to_kelvin(temp)
        results.append({
            "unit": "F",
            "name": UNIT_LABELS["F"]["name"],
            "symbol": UNIT_LABELS["F"]["symbol"],
            "value": round(f_val, 2),
            "formatted": f"{f_val:.2f}"
        })
        results.append({
            "unit": "K",
            "name": UNIT_LABELS["K"]["name"],
            "symbol": UNIT_LABELS["K"]["symbol"],
            "value": round(k_val, 2),
            "formatted": f"{k_val:.2f}"
        })

    elif normalized_unit == "F":
        c_val = fahrenheit_to_celsius(temp)
        k_val = fahrenheit_to_kelvin(temp)
        results.append({
            "unit": "C",
            "name": UNIT_LABELS["C"]["name"],
            "symbol": UNIT_LABELS["C"]["symbol"],
            "value": round(c_val, 2),
            "formatted": f"{c_val:.2f}"
        })
        results.append({
            "unit": "K",
            "name": UNIT_LABELS["K"]["name"],
            "symbol": UNIT_LABELS["K"]["symbol"],
            "value": round(k_val, 2),
            "formatted": f"{k_val:.2f}"
        })

    elif normalized_unit == "K":
        c_val = kelvin_to_celsius(temp)
        f_val = kelvin_to_fahrenheit(temp)
        results.append({
            "unit": "C",
            "name": UNIT_LABELS["C"]["name"],
            "symbol": UNIT_LABELS["C"]["symbol"],
            "value": round(c_val, 2),
            "formatted": f"{c_val:.2f}"
        })
        results.append({
            "unit": "F",
            "name": UNIT_LABELS["F"]["name"],
            "symbol": UNIT_LABELS["F"]["symbol"],
            "value": round(f_val, 2),
            "formatted": f"{f_val:.2f}"
        })

    return {
        "input": {
            "value": round(temp, 2),
            "formatted": f"{temp:.2f}",
            "unit": normalized_unit,
            "symbol": UNIT_LABELS[normalized_unit]["symbol"],
            "name": UNIT_LABELS[normalized_unit]["name"]
        },
        "results": results
    }
