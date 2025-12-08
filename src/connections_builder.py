import time


def build_connections(slack):
    users = slack.paginated("users.list", "members", {"limit": 200})
    users_map = {u["id"]: u for u in users if not u.get("deleted", False)}

    channels = slack.paginated(
        "conversations.list",
        "channels",
        {"limit": 200, "types": "public_channel,private_channel,mpim,im"},
    )

    result = []
    for channel in channels:
        channel_id = channel["id"]
        try:
            members_resp = slack._request(
                "conversations.members", {"channel": channel_id}
            )
            members = members_resp.get("members", [])
        except Exception:
            members = []
            
        result.append(
            {
                "id": channel_id,
                "name": channel.get("name"),
                "is_private": channel.get("is_private"),
                "is_im": channel.get("is_im"),
                "is_mpim": channel.get("is_mpim"),
                "members": [
                    users_map.get(uid, {"id": uid}) for uid in members
                ],
            }
        )

    return {
        "timestamp": int(time.time()),
        "channels": result,
    }
