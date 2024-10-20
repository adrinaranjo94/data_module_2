# Change Data Capture (CDC) Project

This project implements different **Change Data Capture (CDC)** strategies using MySQL and MongoDB. The CDC strategies supported are:

- **Triggers-based**
- **Binlog-based**
- **Differential queries-based**

## Project Structure

    ```bash
    /cdc_project
        /destinations
            base_destination.py         # Abstract base class for data destinations
            mongo_destination.py        # Logic for inserting/updating in MongoDB
        /strategies
            differential.py             # Differential query-based CDC strategy
            binlog.py                   # Binlog-based CDC strategy
            triggers.py                 # Trigger-based CDC strategy
        /db_init
            mysql_init.py               # MySQL initialization logic
            mongo_init.py               # MongoDB initialization logic
        container.py                         # Main file handling commands and strategies
    ```

## Getting Started

- Clone the repository

  ```bash
  git clone https://github.com/yourusername/cdc_project.git
  cd cdc_project
  ```

- Set up a virtual enviroment:

  ```bash
  python3 -m venv venv
  source venv/bin/activate   # On Windows use `venv\Scripts\activate`
  ```

- Install dependencies

  ```bash
  pip install -r requirements.txt
  ```

- Docker setup: Ensure that you have Docker installed and running on your system, as this project uses Docker containers for MySQL and MongoDB.

- Run the application: The project uses the following commands to manage and apply CDC strategies.

## Commands

- **Create MySQL and MongoDB containers**:

  ```bash
  python container.py -create
  ```

  This command starts both MySQL and MongoDB containers.

- **Initialize the database and apply a CDC strategy:**

  ```bash
  python main.py -init --strategy [differential|binlog|triggers] --to [mongo]
  ```

  This command initializes the MySQL database and applies the specified CDC strategy.

  - `trigger`: Apply the trigger-based CDC strategy.
  - `binlog`: Apply the binlog-based CDC strategy.
  - `differential`: Apply the differential queries-based CDC strategy.
  - `--to mongo`: Specifies MongoDB as the destination for the captured data.

- **Delete the MySQL and MongoDB containers:**
  ```bash
  python container.py -delete
  ```
  This command stops and removes the MySQL and MongoDB containers.

## CDC Strategies

### Trigger-based CDC

This strategy uses MySQL triggers to capture insert and update events in the `posts` table. The triggers log changes to an `audit_logs` table. The application then reads from the `audit_logs` and inserts or updates the captured changes into MongoDB.

### Binlog-based CDC

This strategy uses the MySQL binlog to capture row-level events (inserts, updates, and deletes). The `mysql-replication` library streams binlog events and inserts or updates the data in MongoDB. The strategy ensures that changes are captured in near real-time as they happen.

### Differential Query-based CDC

This strategy periodically queries the MySQL database to capture changes based on the updated_at timestamp. It queries for records updated in the last minute using:

```sql
WHERE updated_at >= NOW() - INTERVAL 1 MINUTE
```

Changes are then inserted or updated in MongoDB (or another specified destination).

### Additional information

#### MySQL Initialization

MySQL initialization includes creating the necessary tables and setting the timezone (by default, `Europe/Madrid`, but this can be modified in the `mysql_init`.py file).

Example of the MySQL table posts:

```sql
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stamp VARCHAR(20),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### MongoDB Initialization

The `init_mongo()` function drops the existing MongoDB database (`cdc_database`) if it exists and creates a fresh one. It also creates a default collection called `cdc_collection`.

- **MongoDB:** MongoDB is included in the setup but does not require initialization for this example.
