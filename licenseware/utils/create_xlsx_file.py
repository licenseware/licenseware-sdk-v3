# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from licenseware.config.config import Config

import os
import pandas as pd
from typing import List, Dict, Union


def create_xlsx_file(
    tenant_id: str,
    filename: str,
    sheets: Dict[str, Union[dict, List[dict]]],
    config: Config,
):

    dirpath = os.path.join(config.FILE_UPLOAD_PATH, tenant_id)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    filepath = os.path.join(dirpath, filename or "data.xlsx")
    assert filepath.endswith(".xlsx")

    xlwriter = pd.ExcelWriter(filepath)

    for sheet, data in sheets.items():
        if not data:
            continue
        _df = pd.DataFrame.from_records([data] if isinstance(data, dict) else data)
        _df.to_excel(xlwriter, sheet_name=sheet[0:30], index=False)

    xlwriter.save()
    xlwriter.close()

    return dirpath, filename
