# Sample API Requests

Use the Swagger interface at `/docs` to test these.

## 1. Create Student

POST `/students`

```json
{
  "student_id": 101,
  "name": "Rahul Sharma",
  "date_of_birth": "2005-06-15",
  "email": "rahul@example.com",
  "phone": "9876543210",
  "course": "B.Tech CSE",
  "address": "Kolkata",
  "enrollment_date": "2023-08-01"
}
```

## 2. Create Another Student

```json
{
  "student_id": 102,
  "name": "Ananya Das",
  "date_of_birth": "2004-11-20",
  "email": "ananya@example.com",
  "phone": "9123456780",
  "course": "B.Tech CSE",
  "address": "Kolkata",
  "enrollment_date": "2023-08-01"
}
```

## 3. List Students

GET `/students`

## 4. Filter by Name

GET `/students?name=Rahul`

## 5. Filter by Course

GET `/students?course=B.Tech%20CSE`

## 6. Get One Student

GET `/students/101`

## 7. Update Student

PUT `/students/101`

```json
{
  "phone": "9999999999",
  "course": "B.Tech Computer Science"
}
```

## 8. Delete Student

DELETE `/students/102`
