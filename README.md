# Python CRUD Application with PostgreSQL and psycopg

This is a console-based CRUD (Create, Read, Update, Delete) application in Python that uses a PostgreSQL database for data storage, implements batch data generation via SQL, and uses the `psycopg` library to interact with the database following the MVC architectural pattern.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Python 3.x installed
* PostgreSQL installed and running
* psycopg and python-dotenv

## Getting Started

### Step 2: Configure the Database Connection

Create a `.env` file in the root directory based on the provided `.env.example` file and provide your PostgreSQL database details:

```env
DB_HOST=localhost
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_PORT=5432
```

### Step 3: Run the Application

Execute the following command to run the application:

```bash
python main.py
```
