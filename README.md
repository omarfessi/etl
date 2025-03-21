# ETL Pipeline for Data Processing

## Overview
This project is an ETL (Extract, Transform, Load) pipeline designed to process and manage data. The pipeline extracts data from excel sheets, transforms it into a star schema (fact and dimensions tables), and loads it into postgres, and finally create a BI layer in duckdb to be consumed in PowerBI dashboard.

## Architecture Diagram

![Architecture Diagram ](archi.png?raw=true "Diagram")

## Project Structure
```
├── main.py                 # Main ETL script
├── sql_dml.py              # SQL DML statements (INSERT queries)
├── sql_ddl.py              # SQL DDL statements (table creation)
├── postgres_manager.py     # PostgreSQL connection management
├── config.py               # Configuration (file paths, column mappings, data types)
├── .env                    # Environment variables
├── .pre-commit-config.yaml # Pre-commit hooks
```


## Prerequisites

Ensure you have the following installed:
* Python 3.12+
* Docker (to run PostgreSQL container)
* Duckdb
* Required Python packages (see `requirements.txt`)



## Installation
1. Clone this repository:
2. Create and activate a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate    # On Windows
    ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables by creating a `.env` file in the project root:
   ```env
   DB_HOST=127.0.0.1
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=<your_password>
   ```

## Running PostgreSQL with Docker
Before running the ETL pipeline, start a PostgreSQL container:
```bash
docker run --name postgres-container -p 5432:5432 -e POSTGRES_PASSWORD=<your_password> -v data:/var/lib/postgresql/data -d postgres:17-alpine
```

## How to Run the ETL Pipeline
1. Ensure the PostgreSQL database is running.
2. Run the ETL pipeline:
   ```bash
   python main.py
   ```

## Pre-commit Hook Configuration
This project uses pre-commit hooks for code formatting and linting.
To set up pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

## How It Works
### Data Extraction
- Reads data from an Excel file using `pandas`.
- Applies optional data type conversions and column renaming.

### Data Transformation
- Extracts and processes the `date` column to derive time-based features.

### Data Loading
- Creates the `date_dim` table in PostgreSQL (if not exists).
- Inserts transformed date information into the `date_dim` table.

## Database Schema
### Table: `date_dim`
| Column      | Type         | Description                |
|------------|-------------|----------------------------|
| event_date | DATE        | Primary key (event date)   |
| day        | INTEGER     | Day of the month          |
| week       | INTEGER     | ISO week number           |
| month      | INTEGER     | Month number              |
| year       | INTEGER     | Year                      |
| dayofweek  | INTEGER     | Day of the week (0-6)     |

## Troubleshooting
- **Database Connection Error**: Ensure PostgreSQL is running and credentials in `.env` are correct.
- **Excel File Not Found**: Verify `file_path` in `config.py`.
- **Docker Container Issues**: Ensure you have Docker installed and running
