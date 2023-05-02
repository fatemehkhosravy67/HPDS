# HPDS
# RAM Usage API

This is a simple REST API that allows you to retrieve the RAM usage history of a computer system.

## Features
- Retrieve the n most recent RAM usage data points, where n is a positive integer.
- RAM usage data includes total RAM, free RAM, used RAM, and timestamp of measurement.

## Technologies Used
- Python 3.9
- FastAPI
- SQLite
- SQLAlchemy

## How to Run
1. Install Python 3.9 or higher.
2. Clone this repository.
3. Create a virtual environment: `python3 -m venv env`.
4. Activate the virtual environment: `source env/bin/activate` (Linux/MacOS) or `env\Scripts\activate` (Windows).
5. Install the required packages: `pip install -r requirements.txt`.
6. Run backend.py `python backend/backend.py`
7. Start the server: `uvicorn main:app --reload`.
8. The server should now be running on [localhost:8000/](http://localhost:8000/).
9. The API docs are available at [localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs).


## Testing the project
### Unit testing
For testing, run this command in the root folder of the project:
```shell
pytest
```

## API Documentation
- `GET /ram_usage/?n={n}`: Retrieves the n most recent RAM usage data points. n should be a positive integer.

## Database Schema
The database has one table, `ram_usage`, with the following schema:

| Column    | Type          | Description                                                  |
|-----------|---------------|--------------------------------------------------------------|
| id        | integer       | Primary key                                                  |
| total     | float         | Total amount of RAM available                                |
| free      | float         | Amount of free RAM                                           |
| used      | float         | Amount of RAM being used                                      |
| timestamp | datetime      | Time when the RAM usage was measured (default: current time) |
