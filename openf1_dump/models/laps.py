import requests
from openf1_dump.mongo import get_collection
from openf1_dump import api

def get_laps(session_key: int, driver_number: int):
    print(f"Querying laps for session {session_key} driver {driver_number}")
    try:
        return api.fetch(f"laps?session_key={session_key}&driver_number={driver_number}")
    except Exception as e:
        # https://api.openf1.org/v1/laps?session_key=9480&driver_number=10 always returns in an internal error
        # Probably because of the DNF in lap 1 in actual race. Return no laps in that case.
        return []

def ingest_laps(session_key: int, driver_number: int):
    laps = get_laps(session_key, driver_number)
    if len(laps) == 0:
        print(f"No laps found for driver {driver_number} in session {session_key}")
        return
    collection = get_collection("laps")
    collection.delete_many({"session_key": session_key, "driver_number": driver_number})
    collection.insert_many(laps)
    print("Inserted laps")