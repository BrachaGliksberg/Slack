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
    
    def send_request(self, method, params):
        return requests.get(
            self.BASE_URL + method,
            headers=self.headers,
            params=params,
            timeout=30
        )
    
    def handle_http_status(self, resp, attempt):
        if resp.status_code != 200:
            if attempt == self.max_retries:
                resp.raise_for_status()
            return False  
        return True
    
    def parse_json(self, resp):
        data = resp.json()
        if data.get("ok"):
            return data
        
        if data.get("error") in ("ratelimited", "internal_error", "timeout"):
            return None
        
        raise RuntimeError(f"Slack API error: {data.get('error')}")
    
    def wait_retry(self, attempt):
        time.sleep(2 ** attempt)

    def request(self, method: str, params=None):
        params = params or {}

        for attempt in range(1, self.max_retries + 1):
            resp = self.send_request(method, params)
            if not self.handle_http_status(resp, attempt):
                self.wait_retry(attempt)
                continue

            result = self.parse_json(resp)
            if result is None:
                self.wait_retry(attempt)
                continue

            return result 

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
