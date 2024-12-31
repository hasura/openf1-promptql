import requests
from openf1_dump.mongo import get_collection
from openf1_dump import api

def get_car_data(session_key: int, driver_number: int):
    print(f"Querying car data for session {session_key} driver {driver_number}")
    return api.fetch(f"car_data?session_key={session_key}&driver_number={driver_number}")

def ingest_car_data(session_key: int, driver_number: int):
    car_data = get_car_data(session_key, driver_number)
    if len(car_data) == 0:
        print("No car data found")
        return
    collection = get_collection("car_data")
    collection.delete_many({"session_key": session_key, "driver_number": driver_number})
    collection.insert_many(car_data)
    print("Inserted car data")
    