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
