import time


def build_connections(slack):
    channels = get_channels(slack)
    users_map = get_users(slack)
    result = []

    for channel in channels:
        members = get_channel_members(slack, channel["id"])
        channel_object = build_channel_object(channel, users_map, members)
        result.append(channel_object)

    return {
        "timestamp": int(time.time()),
        "channels": result,
    }

def get_users(slack):
    users = slack.paginated("users.list", "members", {"limit": 200})
    users_map = {user["id"]: user for user in users if user.get("deleted", True)}
    return users_map

def get_channels(slack):
    channels = slack.paginated(
        "conversations.list",
        "channels",
        {"limit": 200, "types": "im, mpim, private_channel, public_channel"},
    )
    return channels

def get_channel_members(slack, channel_id):
    try:
        resp = slack.request("conversations.members", {"channel": channel_id})
        return resp.get("members", [])
    except Exception:
        return []

def build_channel_object(channel, users_map, members):
    return {
        "id": channel["id"],
        "name": channel.get("name"),
        "members": [users_map.get(uid, {"id": uid}) for uid in members],
    }
