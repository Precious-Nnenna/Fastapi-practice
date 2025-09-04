from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    grade: str

students = {}

@app.post("/students")
def add_student(student: Student):
    student_id = len(students) + 1
    students[student_id] = student.model_dump()
    return {"id": student_id, **student.model_dump()}   


@app.get("/students")
def list_students(grade: str = None):
    if grade:
        return [ {"id": sid, **sdata} for sid, sdata in students.items() if sdata["grade"] == grade ]
    
    return list(students.values())

#if grade is provided, filter students by grade
#else return all students
#if grade:
#   result = []
#   for sid, sdata in students.items():
#       if sdata["grade"] == grade:
#          student_info = {"id": sid, **sdata}
#          result.append(student_info)
#   return result


@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    if student_id not in students:
        return{"Error": "Student not found"}
    
    return{"id": student_id, **students[student_id]}


@app.put("/students/{student_id}")
def update_student_data(student_id: int, student: Student):
    if student_id not in students:
        return{"Error": "Student not found"}
    
    students[student_id] = student.model_dump()
    
    return {"id": student_id, **student.model_dump()}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student not found"}
    del students[student_id]
    return {"message": "Student deleted successfully"}