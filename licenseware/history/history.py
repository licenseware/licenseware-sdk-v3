import inspect
from typing import Callable, Union

from licenseware.constants.default_collections import Collections
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository
from licenseware.utils.logger import log as logg

from .metadata import create_metadata, get_metadata
from .schemas import entities_validator, remove_entities_validator
from .step import save_filecontent_validation, save_filename_validation, save_step


def add_entities(event_id: str, entities: list, repo: MongoRepository):
    """
    Add reference ids to entities like databases, devices etc
    Usage:
    ```py
        def processing_func(*args, **kwargs):
            entity_id1, entity_id2 = get_some_entities()
            history.add_entities(event_id, entities=[entity_id1, entity_id2], repo=repo)
    ```
    Where `entity_idx` is an uuid4 string.

    """

    return repo.update_one(
        filters={"event_id": event_id},
        data={"entities": entities},
        append=True,
        data_validator=entities_validator,
        collection=Collections.MONGO_COLLECTION_HISTORY_NAME,
    )


def remove_entities(
    event_id: str,
    entities: list,
    repo: MongoRepository,
):
    """
    Remove reference ids to entities like databases, devices etc from history
    Usage:
    ```py
        def processing_func(*args, **kwargs):
            entity_id1, entity_id2 = get_some_entities()
            history.add_entities(event_id, entities=[entity_id1, entity_id2], repo=repo)
    ```
    Where `entity_idx` is an uuid4 string.

    """
    repo.update_one(
        filters={"event_id": event_id},
        data_validator=remove_entities_validator,
        data={"$pull": {"entities": {"$in": entities}}},
        collection=Collections.MONGO_COLLECTION_HISTORY_NAME,
    )

    return repo.find_one(
        filters={"event_id": event_id},
        collection=Collections.MONGO_COLLECTION_HISTORY_NAME,
    )


def log_success(
    func: Union[Callable, str],
    tenant_id: str,
    event_id: str,
    uploader_id: str,
    app_id: str,
    filepath: str,
    repo: MongoRepository,
    on_success_save: str = None,
    step: str = None,
    func_source: str = None,
):
    """
    Log in history a processing success event.
    Usage:
    ```py
        def processing_func(*args, **kwargs):
            # some processing here
            history.log_success(
                func=processing_func,  # for classes use self.func
                tenant_id=tenant_id,
                event_id=event_id,
                uploader_id=uploader_id,
                filepath=filepath,
                repo=repo,
                on_success_save="Entities added successfully"
            )
            # some processing here
    ```
    """

    if isinstance(func, str):
        func_name = func
        step = step or func
        func_source = func_source
    else:
        func_name = func.__name__
        step = func.__doc__.strip() if func.__doc__ else func.__name__
        func_source = (
            str(inspect.getmodule(func))
            .split("from")[1]
            .strip()
            .replace("'", "")
            .replace(">", "")
        )

    metadata = create_metadata(
        step=step,
        tenant_id=tenant_id,
        event_id=event_id,
        uploader_id=uploader_id,
        app_id=app_id,
        filepath=filepath,
        func_name=func_name,
        func_source=func_source,
    )

    save_step(
        metadata=metadata,
        response=None,
        repo=repo,
        on_success_save=on_success_save,
        on_failure_save=None,
        raised_error=False,
    )
    return metadata


def log_failure(
    func: Union[Callable, str],
    tenant_id: str,
    event_id: str,
    uploader_id: str,
    app_id: str,
    filepath: str,
    error_string: str,
    traceback_string: str,
    repo: MongoRepository,
    on_failure_save: str = None,
    step: str = None,
    func_source: str = None,
    **overflow,
):
    """
    Log in history a processing failure event.
    Usage:
    ```py
        def processing_func(*args, **kwargs):
            # some processing here
            try:
                raise Exception("Something bad happened")
            except Exception as error:
                history.log_failure(
                    func=processing_func, # for classes use self.func
                    tenant_id=tenant_id,
                    event_id=event_id,
                    uploader_id=uploader_id,
                    filepath=filepath,
                    error_string=str(error),
                    traceback_string=str(traceback.format_exc())
                )
            # some processing here
    ```

    """

    if isinstance(func, str):
        func_name = func
        step = step or func
        func_source = func_source
    else:
        func_name = func.__name__
        step = func.__doc__.strip() if func.__doc__ else func.__name__
        func_source = (
            str(inspect.getmodule(func))
            .split("from")[1]
            .strip()
            .replace("'", "")
            .replace(">", "")
        )

    metadata = create_metadata(
        step=step,
        tenant_id=tenant_id,
        event_id=event_id,
        uploader_id=uploader_id,
        app_id=app_id,
        filepath=filepath,
        func_name=func_name,
        func_source=func_source,
    )

    save_step(
        metadata=metadata,
        response={"error": error_string, "traceback": traceback_string},
        repo=repo,
        on_success_save=None,
        on_failure_save=on_failure_save,
        raised_error=True,
    )

    return metadata


def log_filename_validation(
    tenant_id: str,
    event_id: str,
    uploader_id: str,
    app_id: str,
    filename_validation: list,
    repo: MongoRepository,
):

    return save_filename_validation(
        tenant_id=tenant_id,
        event_id=event_id,
        uploader_id=uploader_id,
        app_id=app_id,
        filename_validation=filename_validation,
        repo=repo,
    )


def log_filecontent_validation(
    tenant_id: str,
    event_id: str,
    uploader_id: str,
    app_id: str,
    filecontent_validation: list,
    filepaths: list,
    repo: MongoRepository,
):
    return save_filecontent_validation(
        tenant_id=tenant_id,
        event_id=event_id,
        uploader_id=uploader_id,
        app_id=app_id,
        filecontent_validation=filecontent_validation,
        filepaths=filepaths,
        repo=repo,
    )


# TODO - it's a bit messy
# def log(
#     *dargs,
#     on_success_save: str = None,
#     on_failure_save: str = None,
#     on_failure_return: Any = None,
# ):
#     """
#         Log processing events by decorating processing function/methods.

#         Usage:
#         ```py
#             @history.log
#             def processing_function(filepath, event_id, uploader_id, tenant_id):
#                 # some processing here
#                 return "some data"
#         ```

#         Parameters: filepath, event_id, uploader_id, tenant_id are REQUIRED!
#         Required parameters can be put on self in class like:

#         ```py
#             class ProcessingClass:

#                 def __init__(self, event):
#                     self.event_id = event["event_data"]["event_id"]
#                     self.uploader_id = event["event_data"]["uploader_id"]
#                     self.tenant_id = event["event_data"]["tenant_id"]

#                 @history.log(on_failure_return={})
#                 def proc_func_within_class(self, filepath):
#                     print(f"Processing {filepath}...")
#                     raise Exception("Something bad happened")
#                     print("Done!")
#                     return {"k": "v"}
#         ```
#         Either way if needed parameters will not be found an error will be raised by history.log decorator.

#         param: on_success_save - what to save on history logs if function didn't raised any errors
#         param: on_failure_save - what to save on history logs if function raised error
#         param: on_failure_return - if function raised an error return this instead (for safe processing)
#         If you want on failure to return None put it as a string `on_failure_return="None"`
#         Ex:
#         ```
#             @history.log(on_failure_return={})
#             def procFunc(*args, **kwargs):
#                 raise Exception("Failed")

#             >> print(procFunc())
#             >> {}
#         ```

#     Here is an example on how logging a processing event will look like:

#     ```bash

#         {
#             _id: ObjectId('6230670a96defb313cf63fa9'),
#             uploader_id: 'universal_uploader',
#             app_id: 'app',
#             event_id: '6cd474cd-663f-4d1f-891e-e18d0d0ea77e',
#             tenant_id: 'b37761e3-6926-4cc1-88c7-4d0478b04adf',
#             filename_validation: [
#                 {
#                     message: 'Filename is valid',
#                     filename: 'cpuq.txt',
#                     status: 'success'
#                 }
#             ],
#             updated_at: '2022-03-15T10:14:34.470253',
#             filename_validation_updated_at: '2022-03-15T10:14:34.411491',
#             file_content_validation: [
#                 {
#                     message: 'Filename is valid',
#                     filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt',
#                     filename: 'cpuq.txt',
#                     status: 'success'
#                 }
#             ],
#             file_content_validation_updated_at: '2022-03-15T10:14:34.426705',
#             files_uploaded: [
#                 '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf_6cd474cd-663f-4d1f-891e-e18d0d0ea77e_2022-04-14/cpuq.txt'
#             ],
#             processing_details: [
#                 {
#                     step: 'Getting some data out of provided cpuq.txt file',
#                     status: 'success',
#                     traceback: null,
#                     error: null,
#                     Callable: 'processing_function',
#                     success: null,
#                     source: '/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py',
#                     updated_at: '2022-03-15T10:14:34.434117',
#                     filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt',
#                     file_name: "cpuq.txt"
#                 },
#                 {
#                     step: 'Getting some data out of provided cpuq.txt file',
#                     status: 'success',
#                     traceback: null,
#                     error: null,
#                     Callable: 'processing_function_without_decorator',
#                     success: 'Entities added successfully',
#                     source: '/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py',
#                     updated_at: '2022-03-15T10:14:34.454749',
#                     filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt',
#                     file_name: "cpuq.txt"
#                 },
#                 {
#                     step: 'Getting some data out of provided cpuq.txt file',
#                     status: 'failed',
#                     traceback: 'Traceback (most recent call last):\n  File "/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py", line 183, in processing_function_without_decorator\n    raise Exception("Something bad happened")\nException: Something bad happened\n',
#                     error: 'Something bad happened',
#                     Callable: 'processing_function_without_decorator',
#                     success: null,
#                     source: '/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py',
#                     updated_at: '2022-03-15T10:14:34.462103',
#                     filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt',
#                     file_name: "cpuq.txt"
#                 },
#                 {
#                     step: 'proc_func_within_class',
#                     status: 'failed',
#                     traceback: 'Traceback (most recent call last):\n  File "/home/acmt/Documents/lware/licenseware-sdk-v2/licenseware/history/history.py", line 231, in wrapper\n    response = f(*args, **kwargs)\n  File "/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py", line 219, in proc_func_within_class\n    raise Exception("Something bad happened")\nException: Something bad happened\n',
#                     error: 'Something bad happened',
#                     Callable: 'proc_func_within_class',
#                     success: null,
#                     source: '/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py',
#                     updated_at: '2022-03-15T10:14:34.470259',
#                     filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt',
#                     file_name: "cpuq.txt"
#                 }
#             ],
#             entities: [
#                 '5a5be275-cee8-44a6-a11c-0e2b886a820e',
#                 'b137ff5d-90f1-4d45-872d-91b617666b78',
#                 'b3d7a18e-7a6d-4296-8fcc-0464ec243658',
#                 'ebaf16c9-4d88-413d-b395-92b65166ab20'
#             ]
#         }
#     ```

#     """

#     def _decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):

#             metadata = get_metadata(f, args, kwargs)

#             if f.__name__ == "upload_files":
#                 kwargs.update({"event_id": metadata["event_id"]})

#             try:
#                 response = f(*args, **kwargs)

#                 save_step(metadata, response, on_success_save, on_failure_save)
#                 response = add_event_id_to_payload(metadata, response)

#                 # Remove event_data from uploaders response
#                 if not repo.collections.DESKTOP_ENVIRONMENT:
#                     if f.__name__ == "upload_files":
#                         try:
#                             safe_response = deepcopy(response[0])
#                             safe_response.pop("event_data")
#                             return safe_response, response[1]
#                         except Exception as err:
#                             logg.exception(err)

#                 return response
#             except Exception as err:
#                 logg.exception(err)
#                 save_step(
#                     metadata,
#                     {"error": str(err), "traceback": str(traceback.format_exc())},
#                     on_success_save,
#                     on_failure_save,
#                     True,
#                 )

#                 if on_failure_return is not None:
#                     return on_failure_return
#                 elif on_failure_return == "None":
#                     return None
#                 else:
#                     logg.exception(err)
#                     raise err

#         return wrapper

#     return _decorator(dargs[0]) if dargs and callable(dargs[0]) else _decorator
