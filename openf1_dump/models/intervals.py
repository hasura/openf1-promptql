import requests
from openf1_dump.mongo import get_collection
from openf1_dump import api

def get_intervals(session_key: int, driver_number: int):
    print(f"Querying intervals for session {session_key} driver {driver_number}")
    return api.fetch(f"intervals?session_key={session_key}&driver_number={driver_number}")

def ingest_intervals(session_key: int, driver_number: int):
    intervals = get_intervals(session_key, driver_number)
    if len(intervals) == 0:
        print("No intervals found")
        return
    collection = get_collection("intervals")
    collection.delete_many({"session_key": session_key, "driver_number": driver_number})
    collection.insert_many(intervals)
    print("Inserted intervals")