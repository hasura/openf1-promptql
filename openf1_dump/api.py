import requests
from tenacity import retry, stop_after_attempt, wait_exponential

BASE_URL = "https://api.openf1.org/v1"

def print_retry_message(retry_state):
    exception = retry_state.outcome.exception()
    print(f"Exception encountered: {exception}")
    print(f"Retrying in {retry_state.next_action.sleep} seconds... (Attempt {retry_state.attempt_number})")

@retry(stop=stop_after_attempt(5), wait=wait_exponential(), before_sleep=print_retry_message)
def fetch(path: str):
    url = f"{BASE_URL}/{path}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
