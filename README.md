# Students Database CRUD API

EWB Edu Tech Pvt. Ltd. - Internship Project Assignment

## Project

A Python backend application for managing student records using:

- Python
- FastAPI
- SQLite

## Features

- Create student records
- List all students
- Filter students by name or course
- Retrieve one student
- Update student details
- Delete student records
- Input validation
- Missing-record handling
- Persistent SQLite storage
- Interactive Swagger API documentation

## Project Structure

```text
student_crud_api/
├── main.py
├── requirements.txt
├── README.md
├── sample_requests.md
└── .gitignore
```

## Requirements

Python 3.10 or newer is recommended.

## Installation

Open a terminal inside the project folder.

### 1. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the API

```bash
uvicorn main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Database

The SQLite database file `students.db` is created automatically when the application starts.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/students` | Create a student |
| GET | `/students` | List/filter students |
| GET | `/students/{student_id}` | View one student |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |

## Important

Use dummy student data for testing. Do not upload real student personal information.

The optional Ollama AI extension is not included in this first version because the assignment states that the CRUD application is sufficient.
