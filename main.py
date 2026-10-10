from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
import sqlite3
from datetime import date
from typing import Optional

DATABASE = "students.db"

app = FastAPI(
    title="Students Database CRUD API",
    description="EWB Internship Project - Python Backend Development",
    version="1.0.0"
)


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            course TEXT,
            address TEXT,
            enrollment_date TEXT
        )
    """)
    connection.commit()
    connection.close()


initialize_database()


class StudentCreate(BaseModel):
    student_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, min_length=7, max_length=20)
    course: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=250)
    enrollment_date: Optional[date] = None


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, min_length=7, max_length=20)
    course: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=250)
    enrollment_date: Optional[date] = None


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


@app.get("/")
def home():
    return {
        "message": "Students Database CRUD API is running",
        "docs": "/docs"
    }


@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    connection = get_connection()

    existing = connection.execute(
        "SELECT student_id FROM students WHERE student_id = ?",
        (student.student_id,)
    ).fetchone()

    if existing:
        connection.close()
        raise HTTPException(status_code=409, detail="Student ID already exists")

    connection.execute("""
        INSERT INTO students
        (student_id, name, date_of_birth, email, phone, course, address, enrollment_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student.student_id,
        student.name,
        student.date_of_birth.isoformat(),
        str(student.email) if student.email else None,
        student.phone,
        student.course,
        student.address,
        student.enrollment_date.isoformat() if student.enrollment_date else None
    ))

    connection.commit()
    row = connection.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student.student_id,)
    ).fetchone()
    connection.close()

    return row_to_dict(row)


@app.get("/students")
def list_students(
    name: Optional[str] = Query(default=None),
    course: Optional[str] = Query(default=None)
):
    connection = get_connection()

    query = "SELECT * FROM students WHERE 1=1"
    parameters = []

    if name:
        query += " AND name LIKE ?"
        parameters.append(f"%{name}%")

    if course:
        query += " AND course LIKE ?"
        parameters.append(f"%{course}%")

    query += " ORDER BY student_id"

    rows = connection.execute(query, parameters).fetchall()
    connection.close()

    return [row_to_dict(row) for row in rows]


@app.get("/students/{student_id}")
def get_student(student_id: int):
    connection = get_connection()
    row = connection.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    ).fetchone()
    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return row_to_dict(row)


@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    connection = get_connection()

    existing = connection.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    ).fetchone()

    if existing is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Student not found")

    updates = student.model_dump(exclude_unset=True)

    if not updates:
        connection.close()
        raise HTTPException(status_code=400, detail="No fields provided for update")

    field_map = {
        "name": "name",
        "date_of_birth": "date_of_birth",
        "email": "email",
        "phone": "phone",
        "course": "course",
        "address": "address",
        "enrollment_date": "enrollment_date"
    }

    set_parts = []
    values = []

    for field, value in updates.items():
        column = field_map[field]
        if isinstance(value, date):
            value = value.isoformat()
        set_parts.append(f"{column} = ?")
        values.append(str(value) if field == "email" and value else value)

    values.append(student_id)

    connection.execute(
        f"UPDATE students SET {', '.join(set_parts)} WHERE student_id = ?",
        values
    )
    connection.commit()

    row = connection.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    ).fetchone()
    connection.close()

    return row_to_dict(row)


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    connection = get_connection()

    existing = connection.execute(
        "SELECT student_id FROM students WHERE student_id = ?",
        (student_id,)
    ).fetchone()

    if existing is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Student not found")

    connection.execute(
        "DELETE FROM students WHERE student_id = ?",
        (student_id,)
    )
    connection.commit()
    connection.close()

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }
