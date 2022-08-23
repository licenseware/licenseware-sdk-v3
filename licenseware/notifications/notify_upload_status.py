from licenseware.utils.logger import log


def notify_upload_status(event: dict, status: str, app_id: str):

    upload_status = {
        "tenant_id": event["tenant_id"],
        "uploader_id": event["uploader_id"],
        "status": status,
        "app_id": app_id,
    }

    log.info(
        f"APP PROCESSING EVENT: {app_id} in status: {upload_status}\n for uploader {event['uploader_id']} for tenant {event['tenant_id']}"
    )
