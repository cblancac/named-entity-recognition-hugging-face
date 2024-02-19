from typing import Callable, List, Dict

import regex as re

from entidades.engines.regex.entities_from_regex import (
    entities_from_regex,
)

_DIGITS = r"\d{1,3}(?:\.\d{1,3}(?:,\d{1,3})?)?"

def person(text: str) -> List[Dict]:
    """Extract entity PERSON using regex"""
    return []


def user(text: str) -> List[Dict]:
    """Extract entity USER using regex"""
    return []


def loc(text: str) -> List[Dict]:
    """Extract entity LOC using regex"""
    return []


def date(text: str) -> List[Dict]:
    """Extract entity DATE using regex"""
    return []


def percentage(text: str) -> List[Dict]:
    """Extract entity PERCENTAGE using regex"""
    percentage_patter = rf"""
    (?P<num>{_DIGITS}%)
    """
    pattern = re.compile(
        rf"""{percentage_patter}""",
        re.VERBOSE,
    )
    return entities_from_regex(pattern, text, "PERCENTAGE")


def index(text: str) -> List[Dict]:
    """Extract entity INDEX using regex"""
    return []


def org(text: str) -> List[Dict]:
    """Extract entity ORG using regex"""
    return []


def money(text: str) -> List[Dict]:
    """Extract entity MONEY using regex"""
    money_patter = rf"""
    (?P<num>\${_DIGITS})
    """
    pattern = re.compile(
        rf"""{money_patter}""",
        re.VERBOSE,
    )
    return entities_from_regex(pattern, text, "MONEY")


_ALL_METHODS: List[Callable] = [
    person,
    user,
    loc,
    date,
    percentage,
    index,
    org,
    money,
]


def apply_all(text: str) -> List[Dict]:
    matches = list()
    for method in _ALL_METHODS:
        matches += method(text)
    return matches
