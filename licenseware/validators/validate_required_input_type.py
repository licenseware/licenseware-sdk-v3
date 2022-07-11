from typing import Union, List


typemapper= {
    "excel": [".xlsx", ".xls"],
    "csv": [".csv"],
    "xml": [".xml"],
    "text": [".txt"],
    "txt": [".txt"],
}


def validate_required_input_type(filepath: str, required_input_type: Union[str, List[str]], raise_error:bool = True):

    err_msg = f"File is not of required input type: {required_input_type}"

    if isinstance(required_input_type, str):
        required_input_types = [required_input_type]
    elif isinstance(required_input_type, (list, tuple, set,)):
        required_input_types = required_input_type
    else:
        raise ValueError("Only `string` and `iterables`(list, tuple, set) is acepted for `required_input_type` parameter")

    reqitypes = []
    for rtype in required_input_types:
        if rtype in typemapper:
            reqitypes.extend(typemapper[rtype])
        else:
            reqitypes.append(rtype)
    
    if not any(reqtype for reqtype in required_input_type if filepath.endswith(reqtype)):

        if raise_error:
            raise ValueError(err_msg)
        else:
            return err_msg
        
    return True
    
