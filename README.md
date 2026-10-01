# 🌡️ Temperature Converter

> **Prodigy InfoTech — Software Development Internship | Task 01**

A simple and professional web application that converts temperatures between **Celsius, Fahrenheit, and Kelvin**.

## 🚀 Features

- Convert between Celsius, Fahrenheit, and Kelvin
- Displays both converted values instantly
- Results rounded to 2 decimal places
- Input validation and error handling
- Prevents temperatures below absolute zero
- Responsive and minimal UI
- Flask REST API for conversion
- Unit and integration tests

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** Python unittest
- **API:** REST / JSON

## 📁 Project Structure

```text
Prodigy_SD_01/
├── app.py
├── converter.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── tests/
    ├── __init__.py
    ├── test_converter.py
    └── test_app.py

## ⚙️ Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/Sonakshibargali/Prodigy_SD_01.git
cd Prodigy_SD_01
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## 🧪 Run Tests

Run the complete test suite using:

```bash
python -m unittest discover -s tests
```

The tests cover temperature conversion logic, input validation, edge cases, and Flask application routes.

## 🔄 Conversion Formulas

- **Celsius → Fahrenheit:** `(C × 9/5) + 32`
- **Celsius → Kelvin:** `C + 273.15`
- **Fahrenheit → Celsius:** `(F - 32) × 5/9`
- **Kelvin → Celsius:** `K - 273.15`

## 👤 Author

**Sonakshi Bargali**

**Prodigy InfoTech — Software Development Internship**  
**Task 01: Temperature Converter**
