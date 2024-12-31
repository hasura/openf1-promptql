import requests
from openf1_dump.models.sessions import ingest_sessions
from openf1_dump.mongo import get_collection
from openf1_dump import api

def get_meetings(year: int):
    print(f"Querying Meetings for year {year}")
    return api.fetch(f"meetings?year={year}")

def ingest_meetings(year: int):
    meetings = get_meetings(year)
    collection = get_collection("meetings")

    for meeting in meetings:
        meeting_key = meeting["meeting_key"]
        if not collection.find_one({"meeting_key": meeting_key}):
            collection.insert_one(meeting)
            print(f"Inserted meeting {meeting_key}")
        else:
            print(f"Skipped inserting meeting {meeting_key}")
        ingest_sessions(meeting_key)

    print("Inserted Meetings")