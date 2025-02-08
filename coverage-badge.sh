#!/usr/bin/env bash

COVERAGE=$(coverage report --format=total)
badge="![Coverage Badge](https://img.shields.io/badge/coverage-"
REGEX="!\[Coverage Badge\]\(https:\/\/img\.shields\.io\/badge\/coverage-[0-9]{1,3}%25-[a-z]{3,20}\)"

if [ $COVERAGE -lt 50 ]; then
    COLOUR="red"
elif [ $COVERAGE -lt 60 ]; then
    COLOUR="tomato"
elif [ $COVERAGE -lt 70 ]; then
    COLOUR="orange"
elif [ $COVERAGE -lt 80 ]; then
    COLOUR="yellow"
elif [ $COVERAGE -lt 85 ]; then
    COLOUR="greenyellow"
elif [ $COVERAGE -lt 95 ]; then
    COLOUR="green"
else
    COLOUR="forestgreen"
fi

badge="${badge}${COVERAGE}%25-${COLOUR})"

if egrep -q "${REGEX}" README.md; then
    perl -pi -e "s|${REGEX}|${badge}|" README.md
else
    echo "${badge}" >> README.md
fi