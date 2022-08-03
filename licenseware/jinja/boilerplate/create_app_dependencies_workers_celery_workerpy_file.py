import os

from licenseware.jinja.template import create_jinja_template


def create_app_dependencies_workers_celery_workerpy_file(**options):

    return create_jinja_template(
        filename="celery_worker.py",
        template_filename="app.dependencies.workers.celery_worker.py.jinja",
        filepath=os.path.join(
            options.get("rootpath"), "app", "dependencies", "workers"
        ),
        write_to_disk=options.get("write_to_disk"),
    )
