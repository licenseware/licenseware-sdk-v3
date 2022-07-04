from typing import Union, List


def validate_required_input_type(filepath: str, required_input_type: Union[str, List[str]], raise_error:bool = True):

    err_msg = f"File is not of required input type: {required_input_type}"

    if isinstance(required_input_type, str):
        required_input_type = [required_input_type]

    if not any(reqtype for reqtype in required_input_type if filepath.endswith(reqtype)):

        if raise_error:
            raise ValueError(err_msg)
        else:
            return err_msg
        
    return True
    
