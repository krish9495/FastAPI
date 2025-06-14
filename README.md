# 🏥 Patient Management System API

A fully functional REST API built with **FastAPI** for managing patient health records, including dynamic BMI calculation and health verdict classification. The API supports full **CRUD** operations and persists data using a **JSON file**, making it ideal for small-scale clinics, educational demos, or personal projects.

---

## 🚀 Features

- ✅ Add new patients with validated input
- 📋 View all patients or individual patient data
- 🔄 Update specific fields (partial updates supported)
- ❌ Delete a patient by ID
- 📊 Automatically calculates BMI & provides a health verdict
- 🔎 Sort patients by height, weight, or BMI
- 📝 Data stored in a JSON file (no database required)

---

## 🧰 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – High-performance Python web framework
- [Pydantic](https://docs.pydantic.dev/) – Data validation and settings management
- Python 3.9+
- JSON for persistent storage

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/patient-management-api.git
cd patient-management-api

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn
```
## ▶️ Running the API
```bash 
uvicorn main:app --reload
Visit the interactive API docs at: http://127.0.0.1:8000/docs
```

## 📂 API Endpoints
```bash 
Method	Endpoint	Description
GET	/	Welcome message
GET	/about	About the project
GET	/view	View all patient records
GET	/patient/{id}	View a specific patient
POST	/create	Add a new patient
PUT	/edit/{id}	Update patient details (partial OK)
DELETE	/delete/{id}	Delete a patient
GET	/sort	Sort patients by height/weight/BMI
```

## 📘 Example JSON Data (patients.json)
```bash
{
  "P001": {
    "name": "Ananya Verma",
    "city": "Guwahati",
    "age": 28,
    "gender": "female",
    "height": 1.65,
    "weight": 90.0,
    "bmi": 33.06,
    "verdict": "Obese"
  }
}
```

## 📏 Validation Rules
Age: Must be between 1 and 99

Gender: One of male, female, others

Height/Weight: Must be positive

BMI & Verdict: Automatically computed on create/update


## 🧪 Testing
You can test the endpoints using:

Swagger UI: http://127.0.0.1:8000/docs

Postman or any REST client


