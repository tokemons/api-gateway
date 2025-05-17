# Tokemons API-Gateway

## Development:

### Prerequisites

- python 3.13
- uv
- postgresql 17

### Installation

1. **Clone the repository:**

   ```bash
   git clone git@github.com:tokemons/backend.git
   cd backend
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   uv venv
   source .venv/bin/activate
   uv sync --all-groups
   ```


3. **Start the server:**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://0.0.0.0:8000`.

## Usage

- **API Documentation**: Access interactive API documentation at `http://0.0.0.0:8000/docs`.
