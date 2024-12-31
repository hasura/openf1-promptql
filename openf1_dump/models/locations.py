import requests
from openf1_dump.mongo import get_collection
from openf1_dump import api

def get_locations(session_key: int, driver_number: int):
    print(f"Querying locations for session {session_key} driver {driver_number}")
    return api.fetch(f"locations?session_key={session_key}&driver_number={driver_number}")

def ingest_locations(session_key: int, driver_number: int):
    locations = get_locations(session_key, driver_number)
    if len(locations) == 0:
        print("No locations found")
        return
    collection = get_collection("locations")
    collection.delete_many({"session_key": session_key, "driver_number": driver_number})
    collection.insert_many(locations)
    print("Inserted locations")