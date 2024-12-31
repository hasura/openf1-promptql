import requests
from openf1_dump.mongo import get_collection
from openf1_dump import api

def get_weather(session_key: int):
    print(f"Querying weather for session {session_key}")
    return api.fetch(f"weather?session_key={session_key}")

def ingest_weather(session_key: int):
    weather = get_weather(session_key)
    collection = get_collection("weather")
    collection.delete_many({"session_key": session_key})
    collection.insert_many(weather)
    print("Inserted weather")