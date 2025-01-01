import requests
from openf1_dump.models.car_data import ingest_car_data
from openf1_dump.models.intervals import ingest_intervals
from openf1_dump.models.laps import ingest_laps
from openf1_dump.models.locations import ingest_locations
from openf1_dump.models.pits import ingest_pits
from openf1_dump.models.positions import ingest_positions
from openf1_dump.models.stints import ingest_stints
from openf1_dump.mongo import get_collection
from openf1_dump import api

def get_drivers(session_key: int):
    print(f"Querying drivers for session {session_key}")
    return api.fetch(f"drivers?session_key={session_key}")

def ingest_drivers(session_key: int):
    drivers = get_drivers(session_key)
    collection = get_collection("drivers")
    for driver in drivers:
        driver_number = driver["driver_number"]
        session_key = driver["session_key"]
        filter = {"session_key": session_key, "driver_number": driver_number}
        existing_driver = collection.find_one(filter)
        if existing_driver:
            synced = existing_driver.get("__synced")
            if synced == True:
                print(f"Skipping fully synced driver {driver_number} for session {session_key}")
                continue
            print(f"Found partially synced driver {driver_number} for session {session_key}")
        else:
            collection.insert_one(driver)
            print(f"Inserting driver {driver_number} for session {session_key}")

        print(f"Ingesting driver {driver_number} for session {session_key}")

        # Avoid ingesting very large data for now
        # ingest_car_data(session_key, driver_number)
        # ingest_intervals(session_key, driver_number)
        ingest_laps(session_key, driver_number)
        # ingest_locations(session_key, driver_number)
        ingest_pits(session_key, driver_number)
        ingest_positions(session_key, driver_number)
        ingest_stints(session_key, driver_number)

        collection.update_one(
            filter,
            {"$set": {"__synced": True}}
        )
    print("Ingested drivers")