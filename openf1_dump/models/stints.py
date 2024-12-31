import requests
from openf1_dump.mongo import get_collection
from openf1_dump import api

def get_stints(session_key: int, driver_number: int):
    print(f"Querying stints for session {session_key} driver {driver_number}")
    return api.fetch(f"stints?session_key={session_key}&driver_number={driver_number}")

def ingest_stints(session_key: int, driver_number: int):
    stints = get_stints(session_key, driver_number)
    if len(stints) == 0:
        print("No stints found")
        return
    collection = get_collection("stints")
    collection.delete_many({"session_key": session_key, "driver_number": driver_number})
    collection.insert_many(stints)
    print("Inserted stints")