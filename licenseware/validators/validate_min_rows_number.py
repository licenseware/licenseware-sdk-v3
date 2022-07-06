


def validate_min_rows_number(min_rows: int, current_rows:int, raise_error:bool = True):

    err_msg = f"File doesn't have the minimum number of rows: {min_rows}"

    if current_rows < min_rows:
        if raise_error:
            raise ValueError(err_msg)
        else:
            return err_msg

    return True
    
