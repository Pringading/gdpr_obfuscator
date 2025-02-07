import pytest
from coverage_badge.badge import (
    update_readme_badge,
    read_readme,
    replace_badge,
    write_readme,
    get_coverage_percentage,
    get_badge_markdown,
)


@pytest.fixture
def test_readme():
    README = "coverage_badge/test_README.md"
    contents = (
        "# test readme\n"
        + "Some info about the project\n"
        + "![Random Badge](https://img.shields.io/badge/random-blue)\n"
        + "![Coverage Badge](https://img.shields.io/badge/coverage-20%25-red)\n"
        + "Some more info."
    )
    with open(README, "w", encoding="utf-8") as f:
        f.write(contents)
    return README


class TestUpdateReadmeBadge:
    pass


class TestReadReadme:
    @pytest.mark.it('Reads readme')
    def test_reads_readme(self, test_readme):
        expected = (
            "# test readme\n"
            + "Some info about the project\n"
            + "![Random Badge](https://img.shields.io/badge/random-blue)\n"
            + "![Coverage Badge](https://img.shields.io/badge/coverage-20%25-red)\n"
            + "Some more info."
        )
        result = read_readme(test_readme)
        assert result == expected


class TestWriteReadme:
    pass

class TestGetBadgeMarkdown:
    @pytest.mark.it('Test returns expected markup when given an address')
    def test_expected_markup(self):
        expected = "![Coverage Badge](https://img.shields.io/badge/coverage-20%25-red)"
        assert get_badge_markdown(20) == expected
    
