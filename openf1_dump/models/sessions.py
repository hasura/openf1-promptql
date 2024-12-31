import requests
from openf1_dump.models.drivers import ingest_drivers
from openf1_dump.models.weather import ingest_weather
from openf1_dump.mongo import get_collection
from openf1_dump import api

def get_non_practice_sessions(meeting_key: int):
    print(f"Querying sessions for meeting {meeting_key}")
    sessions = api.fetch(f"sessions?meeting_key={meeting_key}")
    return [session for session in sessions if session['session_type'] != 'Practice']

def ingest_sessions(meeting_key: int):
    sessions = get_non_practice_sessions(meeting_key)
    collection = get_collection("sessions")

    for session in sessions:
        session_key = session["session_key"]
        filter = {"session_key": session_key}
        existing_session = collection.find_one(filter)
        if existing_session:
            synced = existing_session.get("__synced")
            if synced == True:
                print(f"Skipping fully synced session {session_key}")
                continue
            print(f"Found partially synced session {session_key}")
        else:
            collection.insert_one(session)
            print(f"Inserted session {session_key}")

        print(f"Ingesting session {session_key}")

        ingest_drivers(session_key)
        ingest_weather(session_key)

        collection.update_one(
            filter,
            {"$set": {"__synced": True}}
        )

    print("Inserted sessions")