# Service Now Populate

A comprehensive collection of common PC and Mac problems with their solutions, ready to be imported into ServiceNow. This project includes a web scraper to gather problems and solutions, and a REST API to access the data.

## Features

- Web scraper to collect computer problems and solutions from various sources
- Automatic categorization of problems (hardware, software, network, etc.)
- REST API to access the collected data
- Support for searching and filtering problems
- JSON data storage

## Installation

```bash
# Clone the repository
git clone https://github.com/teleman1991/Service-Now-Populate.git
cd Service-Now-Populate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Scraper

```bash
python src/final_scraper.py
```

This will collect problems and solutions from various sources and save them to `data/computer_problems.json`.

### Starting the API

```bash
uvicorn src.api:app --reload
```

The API will be available at `http://localhost:8000`.

### API Endpoints

- `GET /problems/`: List all problems
  - Query parameters:
    - `category`: Filter by category
    - `search`: Search in problem descriptions and solutions
- `GET /problems/{id}`: Get a specific problem
- `GET /categories/`: List all available categories

## Data Structure

Each problem entry contains:
- Problem description
- Solution
- Category (hardware, software, network, system, storage, or other)

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

MIT
