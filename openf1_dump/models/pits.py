import requests
from openf1_dump.mongo import get_collection
from openf1_dump import api

def get_pits(session_key: int, driver_number: int):
    print(f"Querying pits for session {session_key} driver {driver_number}")
    return api.fetch(f"pit?session_key={session_key}&driver_number={driver_number}")

def ingest_pits(session_key: int, driver_number: int):
    pits = get_pits(session_key, driver_number)
    if len(pits) == 0:
        print("No pits found")
        return
    collection = get_collection("pits")
    collection.delete_many({"session_key": session_key, "driver_number": driver_number})
    collection.insert_many(pits)
    print("Inserted pits")