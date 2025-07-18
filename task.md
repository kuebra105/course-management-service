# Build a Course Management Service with FastAPI
Create a small web API that allows managing courses and participants.

## Tasks (already solved)
Design an API with the following endpoints:
### `GET /courses`
Returns a list of all courses.
### `POST /courses`
Adds a new course (e.g., with `name` and `instructor`).
### `GET /participants`
Returns a list of all participants.
### `POST /participants`
Adds a new participant and assigns them to a course.

## 🚀 Additional Challenges

- Input validation using **Pydantic** --> added in class Course
- Error handling (e.g., return a **404** if a course does not exist) --> already included
- Store data in a simple **in-memory structure** (e.g., list or dictionary) --> already included

## Additional tasks
- Extend validations (e.g., minimum length for names, course names must not be empty)
- Filter participants by course `(GET /participants?course_id=1)`
- Delete courses `(DELETE /courses/{id})`
- Update course details (e.g. a course name) `(PUT /courses/{id})` 
- Update participant info (e.g., change name, change course) `(PUT /participants/{id})`
- Prevent duplicate course names --> prevent duplicate course id
- Prevent adding the same participant to a course twice
- Add timestamps to courses/participants (e.g., created_at) first for courses, then for participants --> there is a python-methode