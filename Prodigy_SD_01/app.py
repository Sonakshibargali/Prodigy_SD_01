"""
Temperature Converter Flask Application
Provides web interface and REST API endpoint for temperature conversion.
"""

from flask import Flask, render_template, request, jsonify
from converter import convert_temperature, TemperatureConversionError

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Renders the temperature converter interface.
    Supports standard HTML form submission (fallback for JS-disabled browsers).
    """
    context = {
        "temperature": "",
        "unit": "C",
        "results": None,
        "error": None,
    }

    if request.method == "POST":
        temp_input = request.form.get("temperature", "").strip()
        unit_input = request.form.get("unit", "C").strip().upper()

        context["temperature"] = temp_input
        context["unit"] = unit_input

        try:
            data = convert_temperature(temp_input, unit_input)
            context["results"] = data["results"]
            context["input_formatted"] = data["input"]["formatted"]
            context["input_symbol"] = data["input"]["symbol"]
        except TemperatureConversionError as err:
            context["error"] = str(err)
        except Exception:
            context["error"] = "An unexpected error occurred. Please try again."

    return render_template("index.html", **context)


@app.route("/api/convert", methods=["POST"])
def api_convert():
    """
    REST API endpoint for temperature conversion via AJAX / Fetch API.
    Expects JSON payload: { "temperature": <value>, "unit": "C" | "F" | "K" }
    """
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Request must be JSON with 'temperature' and 'unit' fields."
        }), 400

    payload = request.get_json(silent=True) or {}
    temperature = payload.get("temperature")
    unit = payload.get("unit")

    if temperature is None or unit is None:
        return jsonify({
            "success": False,
            "error": "Both 'temperature' and 'unit' fields are required."
        }), 400

    try:
        conversion_data = convert_temperature(temperature, unit)
        return jsonify({
            "success": True,
            "data": conversion_data
        }), 200
    except TemperatureConversionError as err:
        return jsonify({
            "success": False,
            "error": str(err)
        }), 400
    except Exception:
        return jsonify({
            "success": False,
            "error": "Internal server error during conversion."
        }), 500


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors gracefully."""
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Endpoint not found"}), 404
    return render_template("index.html", error="Page not found. Redirected to converter."), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors gracefully."""
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Internal server error"}), 500
    return render_template("index.html", error="Internal server error occurred."), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
