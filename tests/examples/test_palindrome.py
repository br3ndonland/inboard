import pytest  # type: ignore

from templatepython.examples import palindrome  # type: ignore


@pytest.mark.parametrize(
    "input_string,output_boolean",
    [
        ("racecar", True),
        ("A man, A Plan, A Canal, Panama", True),
        ("Foo bar", False),
        ("[]", False),
    ],
)
def test_palindrome(input_string: str, output_boolean: bool) -> None:
    assert palindrome.prep_input(input_string) is output_boolean


def test_palindrome_incorrect_input_type() -> None:
    with pytest.raises(AttributeError):
        assert palindrome.prep_input([]) is False  # type: ignore
        raise
