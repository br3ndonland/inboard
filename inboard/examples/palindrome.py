#!/usr/bin/env python3
"""Palindromes"""
import re


def user_input() -> str:
    """Accept user input for palindrome function
    """
    try:
        s = input("Please provide an input to test: ")
        prep_input(s)
        return s
    except Exception:
        raise


def prep_input(s: str) -> bool:
    """Clean and validate user input for palindrome function
    ---
    - Convert user input string to lowercase.
    - Remove any characters other than word and digit.
    - Verify that length is at least 3 characters.
    """
    try:
        s = re.sub(r"[^\w\d]", "", s.lower())
        if len(s) > 2 and palindrome(s):
            print(f"Success! The input {s} is a palindrome.")
            return True
        else:
            print(f"The input {s} is not a palindrome.")
            return False
    except Exception as e:
        print(f"An exception occurred:\n{e}\nPlease try again.")
        raise


def palindrome(s: str) -> bool:
    """Identify palindromes
    ---
    - Accept a string from user input, after validation.
    - Create a new object with the reversed string.
    - Compare forward and reversed strings.
    """
    backwards = s[::-1]
    return s == backwards


if __name__ == "__main__":
    print(user_input())
