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

# log.add(sys.stderr)
