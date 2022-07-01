"""
Docs: 
https://github.com/Delgan/loguru

Basic functionality:


```py

from loguru import logger

log._debug("Debug log")
log.info("Info log")
log.success("Success log")
log.warning("Warning log")
log.error("Error log")
log.critical("Critical log")

try:
    raise Exception("Demo exception")
except:
    log.exception("Exception log")
    log.trace("Trace log")

```


"""

import sys
from loguru import logger as log


_log_level = "DEBUG"
_log_format = """<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>[ <level>{level}</level> ]
<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>
<level>{message}</level>
"""


log.add(
    "app.log",
    rotation="monthly",
    level=_log_level,
    format=_log_format
)

log.add(sys.stderr, format=_log_format)


