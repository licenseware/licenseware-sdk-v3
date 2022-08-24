from marshmallow import Schema, fields

from licenseware.uploader.default_handlers.validators.validate_uuid4 import (
    validate_uuid4,
)


class FileValidationSchema(Schema):
    status = fields.String()
    filename = fields.String()
    message = fields.String()


class ProcessingDetailsSchema(Schema):
    step = fields.String(required=True)
    filepath = fields.String(required=True)
    status = fields.String(required=True)
    # Permisive on_success_save and on_failure_save
    success = fields.Raw(required=False, allow_none=True)
    error = fields.Raw(required=False, allow_none=True)
    traceback = fields.String(required=False, allow_none=True)
    callable = fields.String(required=False, allow_none=True)
    source = fields.String(required=False, allow_none=True)
    updated_at = fields.String(required=True)
    filename = fields.String(required=True)


class HistorySchema(Schema):
    tenant_id = fields.String(required=True, validate=validate_uuid4)
    event_id = fields.String(required=True, validate=validate_uuid4)
    app_id = fields.String(required=True)
    uploader_id = fields.String(required=True)
    filename_validation = fields.List(fields.Nested(FileValidationSchema))
    filecontent_validation = fields.List(fields.Nested(FileValidationSchema))
    files_uploaded = fields.List(fields.String)
    processing_details = fields.List(
        fields.Nested(ProcessingDetailsSchema), allow_none=True
    )
    updated_at = fields.String()
    filename_validation_updated_at = fields.String()
    filecontent_validation_updated_at = fields.String()


class EntitiesSchema(Schema):
    entities = fields.List(fields.Raw, required=True)


def entities_validator(data):
    data = EntitiesSchema(many=True if isinstance(data, list) else False).load(data)
    return data


def history_validator(data):
    data = HistorySchema(many=True if isinstance(data, list) else False).load(data)
    return data


def remove_entities_validator(data):
    # {"$pull": {"entities": {"$in": entities}}}
    assert isinstance(data["$pull"]["entities"]["$in"], list)
    assert len(data["$pull"]["entities"]["$in"]) > 0
    for d in data["$pull"]["entities"]["$in"]:
        assert isinstance(d, str)
    return data
