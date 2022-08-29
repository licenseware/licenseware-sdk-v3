# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

import os
from typing import List

import pandas as pd


def create_csv_file(
    tenant_id: str,
    filename: str,
    data: List[dict],
    config: Config,
):
    assert isinstance(data, list)

    dirpath = os.path.join(config.FILE_UPLOAD_PATH, tenant_id)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    if not filename.endswith(".csv"):  # pragma no cover
        filename = filename + ".csv"

    filepath = os.path.join(dirpath, filename)

    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, quotechar='"')

    return filepath, filename
