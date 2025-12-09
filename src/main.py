import json
import os

from slack_api import SlackAPI
from connections_builder import build_connections


def main():
    token = os.getenv("SLACK_BOT_TOKEN")
    if not token:
        raise SystemExit("Missing SLACK_BOT_TOKEN")

    slack = SlackAPI(token)
    data = build_connections(slack)

    with open("connections.json", "w", encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("connections.json generated.")

if __name__ == "__main__":
    main()
