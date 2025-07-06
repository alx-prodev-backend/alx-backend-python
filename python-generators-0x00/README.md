# Project Report: Python Generator for Streaming SQL Rows

## Overview

This project demonstrates advanced use of Python generators to efficiently stream rows from an SQL database one by one. It focuses on setting up a MySQL database, creating and populating a table with sample data, and preparing for generator-based data streaming to handle large datasets with memory efficiency.

---

## Objectives

- Connect to a MySQL server and manage databases and tables.
- Seed the database table `user_data` with sample CSV data.
- Implement generators to stream data rows iteratively for efficient processing.
- Ensure resource optimization for large datasets by avoiding loading all data at once.

---

## Implementation Details

### 1. Database Setup

- **Database Name:** `ALX_prodev`
- **Table:** `user_data`
- **Table Schema:**
  - `user_id` (Primary Key, VARCHAR(36), UUID format, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)

### 2. Python Script (`seed.py`)

- Functions included:
  - `connect_db()`: Connects to MySQL server without selecting a database.
  - `create_database(connection)`: Creates the `ALX_prodev` database if it does not exist.
  - `connect_to_prodev()`: Connects specifically to the `ALX_prodev` database.
  - `create_table(connection)`: Creates the `user_data` table with required schema.
  - `insert_data(connection, csv_filename)`: Reads data from `user_data.csv` and inserts unique records into the table.

- Data inserted from CSV file example:
  ```csv
  name,email,age
  Dan Altenwerth Jr.,Molly59@gmail.com,67
  Glenda Wisozk,Miriam21@gmail.com,119
  Daniel Fahey IV,Delia.Lesch11@hotmail.com,49
  Ronnie Bechtelar,Sandra19@yahoo.com,22
  Alma Bechtelar,Shelly_Balistreri22@hotmail.com,102
