from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field



app = FastAPI() # an instance of the FastAPI application is created

# field validators: https://realpython.com/python-pydantic/#validating-models-and-fields
# Pydantic modells
class Course(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    instructor: str = Field(min_length=3)

class Participant(BaseModel):
    id: int
    name: str = Field(min_length=3)
    course_id: int

courses: list[Course] = []
participants: list[Participant] = []

@app.get("/courses", response_model=list[Course]) # this indicates a HTTP GET endpoint, 
                                                       # if http://127.0.0.1:8000/courses is called, this function is executed
def get_courses() -> list[Course]:
    return courses

@app.post("/courses", response_model=Course) # defines an HTTP POST endpoint at /courses.
def add_course(course: Course) -> Course:
    # check duplicated ids
    if any(c.id == course.id for c in courses):
        raise HTTPException(status_code=400, detail="Course ID already exists.")
    courses.append(course)
    return course

@app.delete("/courses/{course_id}") # this function is called when the client sends an HTTP DELETE request to the endpoint /courses/{course_id}
                                         # course_id is the function parameter,
                                         # course.id is the field of a single course object in the courses list (the 'id' field)
def delete_course(course_id: int):
    if not any(c.id == course_id for c in courses):
        raise HTTPException(status_code=404, detail="Course not found - there is nothing to delete.") # if no course with the id is found (the course doen not exist)
    for course in courses:
        if course.id == course_id: # if the course is found (the course's id (course.id) and the course_id that is searched for match)...
            courses.remove(course) # it is removed
            # break
            updated_participants = delete_participants_by_course(course_id) # delete_participants_by_course returns a new temporary participant-list
            participants.clear() # the original is cleared in order to...
            participants.extend(updated_participants) # receive the new list


@app.get("/participants", response_model=list[Participant])
def get_participants(course_id: int | None = None) -> list[Participant]: # course-id is an optional parameter, it can be an int, it can be None (not set at all)
    if course_id is not None:
        if not any(c.id == course_id for c in courses):
            raise HTTPException(status_code=404, detail="Course not found.") # if you try to get a list with a course that does not exist? 
        filtered_list: list[Participant] = []
        for participant in participants:
            if participant.course_id == course_id:
                filtered_list.append(participant)
        return filtered_list
    else:
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

def delete_participants_by_course(course_id: int):
    """
    add doc string for function
    - input
    - output 
    - what does the function do 
    - formatting, best practises
    """
    # you can do it without 'global participants' but with a local variable
    temp_list: list[Participant] = []
    for participant in participants:
        if participant.course_id != course_id:
            temp_list.append(participant)
    return temp_list


"""
TESTING-DOUCUMENTATION: this is how I tested the code:

## 1:
1. I successfully added three courses and five participants (200 OK)
   The GET request was executed correctly (200 OK), but the first response was empty (Response body: [ ]). 
   I tried again and it worked (all courses were listed). I was unable to reproduce the 'error'. The same with participants. 
2. I was able to successfully execute the GET/participants request with the parameter course_id=1, the response was complete and correct. 
3. I was able to successfully execute the DELETE/courses/{course_id} request so that the course with course_id=2 was deleted. 
   The response correctly included only the courses with course_id=1 and course_id=3.
4. I was able to successfully execute the GET/participants request with the parameter course_id=2 (200 OK), EVEN though the course has already been deleted (response body: [ ]). 
   This should not be the case and this function should be changed so that an error occurs.
   # global, found_value, 
"""


"""
EDITING-DOUCUMENTATION: this is how I edited the code:

## 1:
1. I added a 404 HTTP status message that is executed when in DELETE course is passed a course_id that is not available. I have also edited and changed the solution with the 'found_value'.
2. I edited the DELETE endpoint and the associated helper function so that a solution with 'global' is no longer necessary.
"""