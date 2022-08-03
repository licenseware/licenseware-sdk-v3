import re
from typing import List


def validate_text_contains_any(
    text: str,
    text_contains_any: List[str],
    regex_escape: bool = True,
    raise_error: bool = True,
):
    """
    Raise exception if contents of the text file don't contain at least one item in text_contains_any list
    """

    if not text_contains_any:
        return True

    for txt_to_find in text_contains_any:
        pattern = re.compile(
            re.escape(txt_to_find) if regex_escape else txt_to_find, flags=re.IGNORECASE
        )
        match = re.search(pattern, text)
        if match:
            return True

    err_msg = f'File must contain at least one of the following keywords: {", ".join(text_contains_any)}'
    if raise_error:
        raise ValueError(err_msg)

    return err_msg
