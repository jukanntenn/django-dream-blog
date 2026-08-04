import pytest
from django.core.management import call_command


class TestSendTestSentryEvent:
    def test_raises_zero_division_error(self):
        with pytest.raises(ZeroDivisionError):
            call_command("sendtestsentryevent")
