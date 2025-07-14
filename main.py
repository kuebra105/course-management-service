from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import time


app = FastAPI() # an instance of the FastAPI application is created

def get_time():
    """
    Returns the current date and time in the format 'Created on YYYY-mm-dd at HH:MM:SS'.

    
    Returns:
        str: formatted timestamp
    """
    timestamp = time.localtime()
    date_format = time.strftime("%Y-%m-%d", timestamp)
    time_format = time.strftime("%H:%M:%S", timestamp)
    return(f"Created on {date_format} at {time_format}.")

# field validators: https://realpython.com/python-pydantic/#validating-models-and-fields
# Pydantic modells
class Course(BaseModel):
    """
    Data model for a Course-object.

    Attributes:
        id (int): unique course ID
        name (str): name of the course (1-100 characters)
        instructor (str): name of the instructor (min. 3 characters)
        created_at (str | None): timestamp of creation
    """
    id: int
    name: str = Field(min_length=1, max_length=100)
    instructor: str = Field(min_length=3)
    created_at: str | None = None

class Participant(BaseModel):
    """
    Data model for a Participant-object.

    Attributes:
        id (int): unique participant ID
        name (str): name of the participant (min. 3 characters)
        course_id (int): associated course ID
        created_at (str | None): timestamp of creation
    """
    id: int
    name: str = Field(min_length=3)
    course_id: int
    created_at: str | None = None

courses: list[Course] = []
participants: list[Participant] = []


@app.get("/courses", response_model=list[Course]) # this indicates a HTTP GET endpoint // if http://127.0.0.1:8000/courses is called, this function is executed
def get_courses() -> list[Course]:
    """
    Returns a list of all existing courses.

    Returns:
        list[Course]: list of courses
    """
    return courses

@app.post("/courses", response_model=Course) # defines an HTTP POST endpoint at /courses.
def add_course(course: Course) -> Course:
    """
    Adds a new course if the ID and name are unique.

    Args:
        course (Course): course data

    Returns:
        Course: the added course

    Raises:
        HTTPException: if ID or name already exist
    """
    if any(c.id == course.id for c in courses): # check duplicated ids
        raise HTTPException(status_code=400, detail="Course ID already exists.")
    if any(c.name == course.name for c in courses): # check duplicated ids
        raise HTTPException(status_code=400, detail="Course name already exists.")
    course.created_at = get_time()
    courses.append(course)
    return course

@app.put("/courses/{course_id}", response_model=Course)
def update_course_info(course_id: int, updated_course: Course):
    """
    Updates the information of an existing course.

    Args:
        course_id (int): ID of the course that is to be updated
        updated_course (Course): new course data

    Returns:
        Course: the updated course

    Raises:
        HTTPException: if the course is not found
    """
    if not any(c.id == course_id for c in courses):
        raise HTTPException(status_code=404, detail="Course not found - there is nothing to update.") # if no course with the id is found (the course does not exist)
    for course in courses:
        if course.id == course_id:
            course.id = updated_course.id
            course.name = updated_course.name
            course.instructor = updated_course.instructor
            update_individual_course_id(course_id, updated_course.id)
            return updated_course

def update_individual_course_id(former_id: int, updated_id: int):
    """
    HELPER FUNCTION: Updates the course ID for all associated participants.

    Args:
        former_id (int): original course ID
        updated_id (int): updated course ID
    """
    for participant in participants:
        if former_id == participant.course_id:
            participant.course_id = updated_id

@app.delete("/courses/{course_id}") # this function is called when the client sends an HTTP DELETE request to the endpoint /courses/{course_id}
                                         # course_id is the function parameter,
                                         # course.id is the field of a single course object in the courses list (the 'id' field)
def delete_course(course_id: int):
    """
    Deletes a course and removes all associated participants.

    Args:
        course_id (int): ID of the course that is to be deleted

    Raises:
        HTTPException: if the course is not found
    """
    course_to_delete = next((c for c in courses if c.id == course_id), None) # the first element of the list for which c.id == course_id is true is returned, if none is found, None is returned
    if course_to_delete is None:
        raise HTTPException(status_code=404, detail="Course not found — nothing to delete.")
    courses.remove(course_to_delete)
    updated_participants = delete_participants_by_course(course_id)
    participants.clear()
    participants.extend(updated_participants)

# helper function
def delete_participants_by_course(course_id: int):
    """
    HELPER FUNCTION: Removes all participants assigned to a specific course.

    Args:
        course_id (int): course ID

    Returns:
        list[Participant]: list of remaining participants
    """
    temp_list: list[Participant] = []
    for participant in participants:
        if participant.course_id != course_id:
            temp_list.append(participant)
    return temp_list


@app.get("/participants", response_model=list[Participant])
def get_participants(course_id: int | None = None) -> list[Participant]: # course-id is an optional parameter, it can be an int, it can be None (not set at all)
    """
    Returns a list of all participants, optionally filtered by course ID.

    Args:
        course_id (int | None): optional course ID for filtering

    Returns:
        list[Participant]: list of participants

    Raises:
        HTTPException: if the course does not exist
    """
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
    """
    Adds a new participant if the course exists and the ID is unique.

    Args:
        participant (Participant): Participant data

    Returns:
        Participant: the added participant

    Raises:
        HTTPException: if course does not exist or ID is already assigned
    """
    if not any(c.id == participant.course_id for c in courses): # course must exist
        raise HTTPException(status_code=404, detail="Course not found. Create a course in order to create participants.")
    if any(p.id == participant.id for p in participants):
        raise HTTPException(status_code=400, detail="Participant ID already exists.")
    participant.created_at = get_time()
    participants.append(participant)
    return participant

@app.put("/participants/{participant_id}")
def update_participant_info(participant_id: int, updated_participant: Participant):
    """
    Updates the information of a existing participant.

    Args:
        participant_id (int): ID of the participant that is to be updated
        updated_participant (Participant): new participant data

    Returns:
        Participant: the updated participant

    Raises:
        HTTPException: if the participant is not found
    """
    if not any(p.id == participant_id for p in participants):
        raise HTTPException(status_code=404, detail="Participant not found - there is nothing to update.") # if no course with the id is found (the course does not exist)
    for participant in participants:
        if participant.id == participant_id:
            participant.id = updated_participant.id
            participant.name = updated_participant.name
            participant.course_id = updated_participant.course_id
            return participant



"""
EDITING-DOUCUMENTATION: this is how I edited the code:

## 1:
1. I added a 404 HTTP status message that is executed when in DELETE course is passed a course_id that is not available. I have also edited and changed the solution with the 'found_value'.
2. I edited the DELETE endpoint and the associated helper function so that a solution with 'global' is no longer necessary.

## 2:
1. I added a PUT endpoint for courses and tested it. It works as expected.
2. I added a PUT endpoint for participants and tested it. It works as expected.
3. I also changed the structure and numbering of the tasks.
4. I have added the function that two courses with the same name cannot be added.
5. The functionality that a participant cannot be added more than once is already given, therefore changes were not necessary.
6. I have set up the timestamps for the courses and participants (I don't particularly like my solution, we can revise it).
7. I also added docstring.
"""