import requests
from openf1_dump.mongo import get_collection
from openf1_dump import api

def get_positions(session_key: int, driver_number: int):
    print(f"Querying positions for session {session_key} driver {driver_number}")
    return api.fetch(f"position?session_key={session_key}&driver_number={driver_number}")

def ingest_positions(session_key: int, driver_number: int):
    positions = get_positions(session_key, driver_number)
    if len(positions) == 0:
        print("No positions found")
        return
    collection = get_collection("positions")
    collection.delete_many({"session_key": session_key, "driver_number": driver_number})
    collection.insert_many(positions)
    print("Inserted positions")