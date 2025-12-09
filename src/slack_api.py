import os
import requests
import time

from dotenv import load_dotenv


load_dotenv()

class SlackAPI:

    BASE_URL = os.getenv("SLACK_BASE_URL", "https://slack.com/api/")

    def __init__(self, token: str, max_retries=3):
        self.token = token
        self.max_retries = max_retries
        self.headers = {"Authorization": f"Bearer {token}"}

    def request(self, method: str, params=None):
        params = params or {}
        for attempt in range(self.max_retries + 1):
            resp = requests.get(
                self.BASE_URL + method,
                headers=self.headers,
                params=params,
                timeout=30
            )
            if resp.status_code != 200:
                if attempt == self.max_retries:
                    resp.raise_for_status()
                time.sleep(2 ** attempt)
                continue
            data = resp.json()
            if data.get("ok"):
                return data
            if data.get("error") in ("ratelimited", "internal_error", "timeout"):
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Slack API error: {data.get('error')}")
        raise RuntimeError("Slack API failed after max retries")

    def paginated(self, method: str, key: str, params=None):
        params = params.copy() if params else {}
        results = []
        cursor = None
        while True:
            data = self.request(method, params)
            results.extend(data.get(key, []))
            cursor = data.get("response_metadata", {}).get("next_cursor")
            if cursor:
                params["cursor"] = cursor
            else:
                break

        return results
