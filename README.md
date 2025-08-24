# Gym Manager Backend

This is the backend for the Gym Manager application, built using FastAPI.

## Requirements

-   Python 3.7+
-   FastAPI
-   Uvicorn

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/gym-manager-backend.git
    cd gym-manager-backend
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m .venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the FastAPI server using Uvicorn:

    ```bash
    fastapi dev src/main.py
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000` to see the API documentation.

## Project Structure

```
gym-manager-backend/
├── app/
│   ├── main.py
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── services/
├── tests/
├── requirements.txt
└── README.md
```

## License

This project is licensed under the MIT License.
