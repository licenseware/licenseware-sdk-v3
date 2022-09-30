import inspect
import time
import datetime
import traceback
from functools import wraps
from typing import Any, Callable, Union

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
    )

    return repo.find_one(
        filters={"event_id": event_id},
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
    func_processing_time: str = None,
    func_args: tuple = None,
    func_kwargs: dict = None,
):

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
        func_processing_time=func_processing_time,
        func_args=func_args,
        func_kwargs=func_kwargs,
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
    func_processing_time: str = None,
    func_args: tuple = None,
    func_kwargs: dict = None,
):

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
        func_processing_time=func_processing_time,
        func_args=func_args,
        func_kwargs=func_kwargs,
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


def log_start_processing(event_id: str, repo: MongoRepository):

    start_time = time.perf_counter()
    return repo.update_one(
        filters={"event_id": event_id}, data={"processing_time": start_time}
    )


def log_end_processing(event_id: str, repo: MongoRepository):

    event = repo.find_one(filters={"event_id": event_id})
    total_seconds = time.perf_counter() - event["processing_time"]
    return repo.update_one(
        filters={"event_id": event_id},
        data={"processing_time": time.strftime("%M:%S", time.gmtime(total_seconds))},
    )


def _get_func_processing_time(start_time: float):
    elapsed = time.perf_counter() - start_time
    func_processing_time = str(datetime.timedelta(seconds=elapsed))
    if func_processing_time.split(":")[0] == "0":
        func_processing_time = "0" + func_processing_time
    return func_processing_time


def log(
    *dargs,
    on_success_save: str = None,
    on_failure_save: str = None,
    on_failure_return: Any = None,
):
    def _decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            try:
                repo = None
                meta = get_metadata(f, args, kwargs)
                repo = MongoRepository(
                    meta.db_connection, collection=meta.config.MONGO_COLLECTION.HISTORY
                )
            except Exception:
                if f.__name__ != "run_processing_pipeline":
                    logg.error(traceback.format_exc())
                repo = None

            start_time = time.perf_counter()
            try:
                response = f(*args, **kwargs)
                if repo is None:
                    return response

                func_processing_time = _get_func_processing_time(start_time)

                log_success(
                    func=meta.step,
                    tenant_id=meta.tenant_id,
                    event_id=meta.event_id,
                    uploader_id=meta.uploader_id,
                    app_id=meta.app_id,
                    filepath=meta.filepath,
                    repo=repo,
                    func_source=meta.source,
                    on_success_save=on_success_save,
                    func_processing_time=func_processing_time,
                    func_args=meta.func_args,
                    func_kwargs=meta.func_kwargs,
                )

                return response
            except Exception as err:

                if repo is None:
                    raise err

                func_processing_time = _get_func_processing_time(start_time)

                log_failure(
                    func=meta.step,
                    tenant_id=meta.tenant_id,
                    event_id=meta.event_id,
                    uploader_id=meta.uploader_id,
                    app_id=meta.app_id,
                    filepath=meta.filepath,
                    func_source=meta.source,
                    repo=repo,
                    error_string=str(err),
                    traceback_string=str(traceback.format_exc()),
                    on_failure_save=on_failure_save,
                    func_processing_time=func_processing_time,
                    func_args=meta.func_args,
                    func_kwargs=meta.func_kwargs,
                )

                if on_failure_return is not None:
                    return on_failure_return
                elif on_failure_return == "None":
                    return None
                else:
                    raise err

        return wrapper

    return _decorator(dargs[0]) if dargs and callable(dargs[0]) else _decorator
