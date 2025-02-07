from coverage import coverage
import re


def update_readme_badge(readme: str="README.md"):
    percentage = 20
    badge = get_badge_markdown(percentage)
    new_readme = ""


def read_readme(readme: str) -> str:
    with open(readme, 'r', encoding='utf-8') as f:
        return f.read()


def replace_badge(contents: str, badge: str) -> str:
    pass


def write_readme(contents: str, file: str) -> None:
    pass


def get_coverage_percentage():
    cov = coverage()
    cov.load()
    total = cov.report()
    return total


def get_badge_markdown(percentage: float) -> str:
    badge = "![Coverage Badge](https://img.shields.io/badge/coverage-"
    if percentage < 45:
        colour = "red"
    elif percentage < 55:
        colour = "tomato"
    elif percentage < 65:
        colour = "orange"
    elif percentage < 75:
        colour = "yellow"
    elif percentage < 80:
        colour = "greenyellow"
    elif percentage < 90:
        colour = "green"
    else:
        colour = "forestgreen"

    badge += f'{str(percentage)}%25-{colour})'
    return badge
