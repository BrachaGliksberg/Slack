from src.connections_builder import build_connections


class FakeSlack:
    def __init__(self):
        self.calls = []

    def paginated(self, method, key, params=None):
        if method == "users.list":
            return [
                {"id": "U1", "name": "alice"},
                {"id": "U2", "name": "bob"},
            ]
        if method == "conversations.list":
            return [
                {"id": "C1", "name": "general", "is_private": False},
                {"id": "C2", "name": "private", "is_private": True},
            ]

    def _request(self, method, params):
        if params["channel"] == "C1":
            return {"ok": True, "members": ["U1", "U2"]}
        if params["channel"] == "C2":
            return {"ok": True, "members": ["U2"]}


def test_build_connections():
    fake = FakeSlack()
    result = build_connections(fake)

    assert "channels" in result
    assert len(result["channels"]) == 2

    general = result["channels"][0]
    assert general["name"] == "general"
    assert len(general["members"]) == 2
