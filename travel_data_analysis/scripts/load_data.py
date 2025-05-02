import pandas as pd
from sqlalchemy import create_engine
import yaml
import os

def load_data_to_postgres(csv_file_path, table_name, db_config):
    """Loads data from CSV to PostgreSQL."""
    try:
        df = pd.read_csv(csv_file_path)
        engine_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        engine = create_engine(engine_string)
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        print(f"Data loaded successfully into table '{table_name}' in PostgreSQL.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """Loads booking and customer data into PostgreSQL."""
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    db_config = config["database"]
    output_path = config['data']['output_path']

    booking_csv_path = os.path.join(output_path, "bookings.csv")
    booking_table_name = "bookings"
    load_data_to_postgres(booking_csv_path, booking_table_name, db_config)

    customer_csv_path = os.path.join(output_path, "customers.csv")
    customer_table_name = "customers"
    load_data_to_postgres(customer_csv_path, customer_table_name, db_config)

if __name__ == "__main__":
    main()