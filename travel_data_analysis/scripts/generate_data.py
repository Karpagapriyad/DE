import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import yaml

fake = Faker()

def generate_fake_booking_data(num_rows):
    """Generates synthetic booking data."""
    data = []
    for _ in range(num_rows):
        customer_id = fake.uuid4()
        destination = random.choice(['Paris', 'London', 'New York', 'Tokyo', 'Rome', 'Sydney', 'Barcelona'])
        start_date = datetime.now() - timedelta(days=random.randint(1, 365))
        booking_date = start_date.strftime('%Y-%m-%d')
        price = round(random.uniform(50, 1000), 2)
        hotel_id = fake.uuid4()
        flight_number = fake.bothify(text='??####')
        num_passengers = random.randint(1, 4)
        data.append({
            'booking_id': fake.uuid4(),
            'customer_id': customer_id,
            'destination': destination,
            'booking_date': booking_date,
            'price': price,
            'hotel_id': hotel_id,
            'flight_number': flight_number,
            'num_passengers': num_passengers
        })
    return pd.DataFrame(data)

def generate_fake_customer_data(num_rows):
    """Generates synthetic customer data."""
    data = []
    for _ in range(num_rows):
        customer_id = fake.uuid4()
        age = random.randint(18, 75)
        city = fake.city()
        country = fake.country()
        email = fake.email()
        data.append({
            'customer_id': customer_id,
            'age': age,
            'city': city,
            'country': country,
            'email': email
        })
    return pd.DataFrame(data)

def main():
    """Generates and saves synthetic travel data to CSV files."""
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    num_bookings = config['data']['num_bookings']
    num_customers = config['data']['num_customers']
    output_path = config['data']['output_path']  # Get output path from config

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    booking_data = generate_fake_booking_data(num_bookings)
    booking_csv_path = os.path.join(output_path, "bookings.csv")
    booking_data.to_csv(booking_csv_path, index=False)
    print(f"Booking data saved to: {booking_csv_path}")

    customer_data = generate_fake_customer_data(num_customers)
    customer_csv_path = os.path.join(output_path, "customers.csv")
    customer_data.to_csv(customer_csv_path, index=False)
    print(f"Customer data saved to: {customer_csv_path}")

if __name__ == "__main__":
    main()