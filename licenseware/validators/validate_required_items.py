from typing import List, Union


def _handle_response(missing_items:List[str], item_type:str, raise_error:bool):
    err_msg = f"File doesn't contain the following needed {item_type}: {missing_items}"
    if len(missing_items) > 0 and raise_error is True:
        raise ValueError(err_msg)
    if len(missing_items) > 0 and raise_error is False:
        return err_msg
    return True


def validate_required_items(items: List[str], item_type:str, required_items: Union[List[str], List[List[str]]], raise_error: bool = True):
    
    if isinstance(required_items[0], str):
        missing_items = list(set.difference(set(required_items), set(items)))
        return _handle_response(missing_items, item_type, raise_error)

    if isinstance(required_items[0], (list, tuple, set,)):
        for rs in required_items:
            missing_items = list(set.difference(set(rs), set(items)))
            res = _handle_response(missing_items, item_type, raise_error=False)
            if res is True:
                return True
    
    err_msg = f"File doesn't contain the following needed {item_type}: {required_items}"
    if raise_error:
        raise ValueError(err_msg)
    return err_msg
