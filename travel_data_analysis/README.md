# Travel Data Analysis Project

## Overview

This project analyzes travel data to identify trends, patterns, and insights that can be used to improve customer experience, optimize pricing, and enhance marketing strategies. It leverages synthetic data generation, PySpark for data processing, PostgreSQL for data storage, and Looker for data visualization.

## Project Structure

travel_data_project/
├── config/ # Configuration files
│ └── config.yaml
├── data/ # Raw data files (CSV)
├── scripts/ # Python scripts
│ ├── generate_data.py # Generates synthetic data
│ ├── process_data.py # Processes data with PySpark
│ └── load_data.py # Loads data into PostgreSQL
├── lookml/ # LookML files (for Looker)
│ ├── model/ # travel_data.model.lkml
│ └── views/ # bookings.view.lkml, customers.view.lkml
├── requirements.txt # Python dependencies
└── README.md # Project overview and instructions



## Technologies Used

*   **Programming Language:** Python
*   **Data Processing:** Apache Spark (PySpark)
*   **Data Storage:** PostgreSQL
*   **Data Visualization:** Looker

## Setup Instructions

1.  **Clone the Repository:**

    ```bash
    git clone <your_repository_url>
    cd travel_data_project
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure PostgreSQL:**

    *   Install PostgreSQL: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
    *   Create a database and user with appropriate permissions:

        ```sql
        CREATE DATABASE your_database_name;
        CREATE USER your_postgres_user WITH PASSWORD 'your_postgres_password';
        GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_postgres_user;
        ```

    *   Adjust `pg_hba.conf` to allow connections (if necessary).

4.  **Configure `config/config.yaml`:**

    *   Update the database connection details:

        ```yaml
        database:
          host: "your_postgres_host"  # e.g., "localhost"
          port: 5432
          database: "your_database_name"
          user: "your_postgres_user"
          password: "your_postgres_password"
        ```

    *   Adjust the `data` section to control data generation and output paths:

        ```yaml
        data:
          num_bookings: 1000
          num_customers: 500
          output_path: "data/"
        ```
     *  Configure spark name.
        ```yaml
        spark:
         app_name: "TravelDataAnalysis"
        ```

## Execution Instructions

1.  **Generate Synthetic Data:**

    ```bash
    python scripts/generate_data.py
    ```

    This will create `bookings.csv` and `customers.csv` in the `data` directory.

2.  **Process Data with PySpark:**

    ```bash
    python scripts/process_data.py
    ```

    This will process the data, perform analysis, and save the transformed data in the `data` directory in parquet format.

3.  **Load Data into PostgreSQL:**

    ```bash
    python scripts/load_data.py
    ```

    This will load the generated data into the `bookings` and `customers` tables in your PostgreSQL database.

## Future Enhancements

*   Implement more sophisticated data cleaning and transformation techniques in PySpark.
*   Develop predictive models for hotel occupancy or price optimization.
*   Integrate additional data sources, such as weather data or social media data.
*   Implement incremental data loading to handle large datasets.
*   Create more comprehensive Looker dashboards with advanced visualizations and user interactivity.
*   Implement workflow orchestration with Apache Airflow or Prefect.

