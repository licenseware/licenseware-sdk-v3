# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

import os
from typing import Dict, List, Union

import pandas as pd


def create_xlsx_file(
    tenant_id: str,
    filename: str,
    data: Dict[str, Union[dict, List[dict]]],
    config: Config,
):

    assert isinstance(data, dict) or isinstance(data, list)
    if not isinstance(data, dict):  # pragma no cover
        data = {"data": data}

    dirpath = os.path.join(config.FILE_UPLOAD_PATH, tenant_id)
    if not os.path.exists(dirpath):  # pragma no cover
        os.makedirs(dirpath)

    if not filename.endswith(".xlsx"):  # pragma no cover
        filename = filename + ".xlsx"

    filepath = os.path.join(dirpath, filename)
    xlwriter = pd.ExcelWriter(filepath)

    for sheet, source in data.items():
        if not source:  # pragma no cover
            continue
        _df = pd.DataFrame.from_records(
            [source] if isinstance(source, dict) else source
        )
        _df.to_excel(xlwriter, sheet_name=sheet[0:30], index=False)

    xlwriter.save()
    xlwriter.close()

    return filepath, filename
