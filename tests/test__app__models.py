from datetime import timezone

from dateutil.parser import parse

from pimon.app import models


class TestForMessage:  # noqa: D101
    dummy_data = {
        "account": "example",
        "uid": 1,
        "sender": "user@example.com",
        "subject": "Non title",
        "received_at": parse("Fri, 12 Aug 2022 01:15:11 -0400"),
    }

    def test_default(self):  # noqa: D102
        msg = models.Message(**self.dummy_data)
        assert msg.received_at.tzinfo == timezone.utc
        assert msg.received_at.hour == 5

    def test_multiple_line_subject(self):  # noqa: D102
        data = dict(**self.dummy_data)
        data["subject"] = "Non \ntitle"
        msg = models.Message(**data)
        assert msg.subject == "Non title"
