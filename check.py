# -*- coding: utf-8 -*-
"""Deciding whether an answer is right.

Comparing program output as plain text does not work for numerics. Two
correct solutions can add the same terms in a different order and differ in
the last digit; insisting on the exact characters would fail the learner for
being right. So every token that looks like a number is compared as a
number, with a tolerance, and everything else as text with the whitespace
normalised.
"""
import re

NUMBER = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")
TOLERANCE = 1e-6


def _tokens(text):
    return (text or "").replace("\r", "").strip().split()


def _same_number(a, b):
    try:
        x, y = float(a), float(b)
    except ValueError:
        return False
    if x != x or y != y:          # NaN: only equal to another NaN
        return x != x and y != y
    return abs(x - y) <= TOLERANCE * max(1.0, abs(y))


def output_matches(got, want):
    """True if the program said what it was supposed to say."""
    a, b = _tokens(got), _tokens(want)
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] == b[i]:
            continue
        if NUMBER.match(a[i]) and NUMBER.match(b[i]):
            if _same_number(a[i], b[i]):
                continue
        return False
    return True


def _normalise(text):
    """For short written answers: spaces and case are not the point."""
    text = (text or "").strip().lower()
    text = re.sub(r"\s+", "", text)
    return text


def text_matches(got, want, alternatives=None):
    candidates = [want]
    if alternatives:
        candidates = candidates + list(alternatives)
    mine = _normalise(got)
    for candidate in candidates:
        if mine == _normalise(candidate):
            return True
    return False
