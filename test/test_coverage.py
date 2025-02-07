import pytest
from coverage_badge.badge import get_badge_markup

class TestGetBadgeMarkup:
    @pytest.mark.it('Test returns expected markup when given an address')
    def test_expected_markup(self):
        expected = "![Coverage Badge](https://img.shields.io/badge/coverage-20%25-red)"
        assert get_badge_markup(20) == expected