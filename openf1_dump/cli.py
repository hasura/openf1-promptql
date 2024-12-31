import argparse
import os

def get_year_input():
    # Parse command-line argument for the year
    parser = argparse.ArgumentParser(description="Fetch and store F1 meetings data for a specific year.")
    parser.add_argument("year", type=int, help="The year of the F1 meetings to fetch")
    args = parser.parse_args()
    return args.year

def should_sample():
    return os.getenv("SAMPLE", "false").lower() == "true"