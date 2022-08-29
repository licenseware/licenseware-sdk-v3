# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

import os
import json
from typing import List, Union


def create_json_file(
    tenant_id: str,
    filename: str,
    data: Union[dict, List[dict]],
    config: Config,
):
    assert isinstance(data, dict) or isinstance(data, list)

    dirpath = os.path.join(config.FILE_UPLOAD_PATH, tenant_id)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    if not filename.endswith(".json"):  # pragma no cover
        filename = filename + ".json"

    filepath = os.path.join(dirpath, filename)

    with open(filepath, "w") as outfile:
        json.dump(data, outfile)

    return filepath, filename
