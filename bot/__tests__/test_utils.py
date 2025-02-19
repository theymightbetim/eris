from bot.utils import is_it_wednesday
from datetime import date

class TestUtils:
    wednesday = date.fromtimestamp(1739945992)
    monday = date.fromtimestamp(173990000)

    def test_today_is_wednesday(self):
        assert is_it_wednesday(self.wednesday) == True

    def test_today_is_monday(self):
        assert is_it_wednesday(self.monday) == False

