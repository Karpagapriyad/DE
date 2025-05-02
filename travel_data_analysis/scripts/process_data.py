from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, datediff, current_date, dayofweek, col, avg, max, min, count, corr
import yaml
import os

def create_spark_session(app_name):
    """Creates a Spark Session."""
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    return spark

def load_data(spark, file_path, file_format="csv", header=True, inferSchema=True):
    """Loads data into a Spark DataFrame."""
    df = spark.read.format(file_format).option("header", header).option("inferSchema", inferSchema).load(file_path)
    return df

def clean_and_transform_bookings(df):
    """Cleans and transforms the booking data."""
    df = df.dropna(subset=["price"])
    df = df.dropDuplicates()
    df = df.withColumn("booking_date", to_date(col("booking_date"), "yyyy-MM-dd"))
    df = df.withColumn("booking_lead_time", datediff(current_date(), col("booking_date")))
    df = df.withColumn("day_of_week", dayofweek(col("booking_date")))
    df = df.withColumn("is_weekend", (col("day_of_week").isin([1, 7])).cast("boolean"))
    return df

def analyze_data(df):
    """Performs data analysis."""
    avg_price_per_destination = df.groupBy("destination").agg(avg("price").alias("average_price"))
    max_price = df.agg(max("price").alias("maximum_price")).collect()[0]["maximum_price"]
    bookings_per_day = df.groupBy("day_of_week").agg(count("*").alias("number_of_bookings"))
    correlation = df.select(corr("booking_lead_time", "price").alias("correlation")).collect()[0]["correlation"]

    print("Average price per destination:")
    avg_price_per_destination.show()
    print(f"Maximum booking price: {max_price}")
    print("Number of bookings per day of the week:")
    bookings_per_day.show()
    print(f"Correlation between booking lead time and price: {correlation}")

    return avg_price_per_destination #Return dataframe needed for Looker

def main():
    """Main function to process travel data with PySpark."""
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    app_name = config['spark']['app_name']
    spark = create_spark_session(app_name)
    output_path = config['data']['output_path']

    booking_csv_path = os.path.join(output_path, "bookings.csv")
    bookings_df = load_data(spark, booking_csv_path)

    transformed_bookings_df = clean_and_transform_bookings(bookings_df)
    transformed_bookings_df.printSchema()
    transformed_bookings_df.show(5)

    # Perform analysis
    avg_price_per_destination = analyze_data(transformed_bookings_df)

    # Example: Save the transformed data to Parquet format
    parquet_output_path = os.path.join(output_path, "processed_bookings")
    transformed_bookings_df.write.parquet(parquet_output_path, mode="overwrite")
    print(f"Transformed bookings data saved to: {parquet_output_path}")

    # Option: Save avg_price_per_destination as well, in parquet or csv if needed for looker
    spark.stop()

if __name__ == "__main__":
    main()