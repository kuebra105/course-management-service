from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic modells
class Course(BaseModel):
    id: int
    name: str
    instructor: str

class Participant(BaseModel):
    id: int
    name: str
    course_id: int

courses: list[Course] = []
participants: list[Participant] = []

@app.get("/courses", response_model=list[Course])
def get_courses() -> list[Course]:
    return courses

@app.post("/courses", response_model=Course)
def add_course(course: Course) -> Course:
    # check duplicated ids
    if any(c.id == course.id for c in courses):
        raise HTTPException(status_code=400, detail="Course ID already exists.")
    courses.append(course)
    return course


@app.get("/participants", response_model=list[Participant])
def get_participants() -> list[Participant]:
    return participants

@app.post("/participants", response_model=Participant)
def add_participant(participant: Participant) -> Participant:
    # course must exist
    if not any(c.id == participant.course_id for c in courses):
        raise HTTPException(status_code=404, detail="Course not found.")
    if any(p.id == participant.id for p in participants):
        raise HTTPException(status_code=400, detail="Participant ID already exists.")
    participants.append(participant)
    return participant
