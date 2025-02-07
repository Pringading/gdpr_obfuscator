from coverage import coverage


cov = coverage()
cov.load()
total = cov.report()
print(total)


def get_badge_markup(percentage: float):
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



