# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

from typing import Dict, List, Union

from .create_csv_file import create_csv_file
from .create_json_file import create_json_file
from .create_xlsx_file import create_xlsx_file

dispacher = {
    "xlsx": create_xlsx_file,
    "json": create_json_file,
    "csv": create_csv_file,
}


def create_file(
    tenant_id: str,
    filename: str,
    filetype: str,
    data: Dict[str, Union[dict, List[dict]]],
    config: Config,
):

    return dispacher[filetype](tenant_id, filename, data, config)
