# Build a Course Management Service with FastAPI
Create a small web API that allows managing courses and participants.

## Tasks
Design an API with the following endpoints:
### `GET /courses`
Returns a list of all courses.
### `POST /courses`
Adds a new course (e.g., with `name` and `instructor`).
### `GET /participants`
Returns a list of all participants.
### `POST /participants`
Adds a new participant and assigns them to a course.

---

## 🚀 Additional Challenges

- Input validation using **Pydantic**
- Error handling (e.g., return a **404** if a course does not exist)
- Store data in a simple **in-memory structure** (e.g., list or dictionary)
