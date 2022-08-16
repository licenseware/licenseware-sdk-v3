import re
from typing import List


def validate_text_contains_all(
    text: str,
    text_contains_all: List[str],
    regex_escape: bool = True,
    raise_error: bool = True,
):
    """
    Raise exception if contents of the text file don't contain all items in text_contains_all list
    """

    if not text_contains_all:  # pragma no cover
        return True

    matches_count = 0
    for txt_to_find in text_contains_all:
        pattern = re.compile(
            re.escape(txt_to_find) if regex_escape else txt_to_find, flags=re.IGNORECASE
        )
        match = re.search(pattern, text)
        if match:
            matches_count += 1

    err_msg = (
        f'File must contain the all following keywords: {", ".join(text_contains_all)}'
    )
    if matches_count < len(text_contains_all):
        if raise_error:
            raise ValueError(err_msg)
        else:
            return err_msg
    return True
