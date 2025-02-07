import pytest
from unittest.mock import patch
from coverage_badge.badge import (
    update_readme_badge,
    read_readme,
    replace_badge,
    write_readme,
    get_badge_markdown,
)


@pytest.fixture
def test_readme():
    README = "coverage_badge/test_README.md"
    contents = (
        "# test readme\n"
        + "Some info about the project\n"
        + "![Random Badge](https://img.shields.io/badge/random-blue)\n"
        + "![Coverage Badge](https://img.shields.io/badge/"
        + "coverage-20%25-red)\n"
        + "Some more info."
    )
    with open(README, "w", encoding="utf-8") as f:
        f.write(contents)
    return README


class TestUpdateReadmeBadge:
    @pytest.mark.it('Updates readme with new percentage')
    @patch('coverage_badge.badge.get_coverage_percentage', return_value=80)
    def test_updates_badge(self, percentage_mock, test_readme):
        expected = (
            "# test readme\n"
            + "Some info about the project\n"
            + "![Random Badge](https://img.shields.io/badge/random-blue)\n"
            + "![Coverage Badge](https://img.shields.io/badge/"
            + "coverage-80%25-green)\n"
            + "Some more info."
        )
        update_readme_badge(test_readme)
        with open(test_readme, 'r', encoding="utf-8") as f:
            assert f.read() == expected


class TestReadReadme:
    @pytest.mark.it('Reads readme')
    def test_reads_readme(self, test_readme):
        expected = (
            "# test readme\n"
            + "Some info about the project\n"
            + "![Random Badge](https://img.shields.io/badge/random-blue)\n"
            + "![Coverage Badge](https://img.shields.io/badge/"
            + "coverage-20%25-red)\n"
            + "Some more info."
        )
        result = read_readme(test_readme)
        assert result == expected


class TestReplaceBadge:
    @pytest.mark.it('If badge not found, adds badge to the end')
    def test_adds_badge_if_not_found(self):
        test_content = "here is some contents"
        test_badge = (
            "![Coverage Badge](https://img.shields.io/badge/"
            + "coverage-20%25-red)"
        )
        result = replace_badge(test_content, test_badge)
        assert test_badge in result

    @pytest.mark.it('If badge found,replaces existing badge')
    def test_replaces_badge_found(self):
        test_badge = (
            "![Coverage Badge](https://img.shields.io/badge/"
            + "coverage-92%25-forestgreen)"
        )
        test_content = (
            "# test readme\n"
            + "Some info about the project\n"
            + "![Random Badge](https://img.shields.io/badge/random-blue)\n"
            + "![Coverage Badge](https://img.shields.io/badge/"
            + "coverage-20%25-red)\n"
            + "Some more info."
        )
        expected = (
            "# test readme\n"
            + "Some info about the project\n"
            + "![Random Badge](https://img.shields.io/badge/random-blue)\n"
            + "![Coverage Badge](https://img.shields.io/badge/"
            + "coverage-92%25-forestgreen)\n"
            + "Some more info."
        )
        result = replace_badge(test_content, test_badge)
        assert result == expected


class TestWriteReadme:
    @pytest.mark.it('writes new content to readme')
    def test_writes_new_content_to_reademt(self, test_readme):
        test_contents = "hello world"
        write_readme(test_readme, test_contents)
        with open(test_readme, 'r', encoding='utf-8') as f:
            assert f.read() == test_contents


class TestGetBadgeMarkdown:
    @pytest.mark.it('Test returns expected markup when given an address')
    def test_expected_markup(self):
        expected = (
            "![Coverage Badge](https://img.shields.io/badge/"
            + "coverage-20%25-red)"
        )
        assert get_badge_markdown(20) == expected
