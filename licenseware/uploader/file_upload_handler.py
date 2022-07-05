import os
import shutil
import asyncio
from typing import Union, IO



class FileUploadHandler:

    def __init__(self, fileorbuffer: Union[str, IO]) -> None:
        self.fileorbuffer = fileorbuffer
        if isinstance(self.fileorbuffer, str):
            if not os.path.isfile(self.fileorbuffer):
                raise FileNotFoundError(f"File {self.fileorbuffer} was not found on disk")
        
        if isinstance(self.fileorbuffer, str):
            self._data = open(self.fileorbuffer, "rb") 
        else:
            attrs = ["read", "seek", "close"]
            if not all(hasattr(self.fileorbuffer, attr) for attr in attrs):
                raise AttributeError(f"Mandatory attributes '{':'.join(attrs)}' not found on provided IO object.")
            self._data = self.fileorbuffer

        self.runsync = True

        co =  asyncio.iscoroutine(self._data.read) 
        cofunc = asyncio.iscoroutinefunction(self._data.read)
        cofuture = asyncio.isfuture(self._data.read)

        if any([co, cofunc, cofuture]):
            self.runsync = False
            
    def sync(self, co):
        return asyncio.get_event_loop().run_until_complete(co)


    def data(self):
        return self

    def read(self, buffering: int = None) -> bytes:
        return self._data.read(buffering) if self.runsync else self.sync(self._data.read(buffering))

    def seek(self, offset: int) -> int:
        return self._data.seek(offset) if self.runsync else self.sync(self._data.seek(offset))

    def reset(self):
        return self._data.seek(0) if self.runsync else self.sync(self._data.seek(0))

    def close(self):
        self._data.close() if self.runsync else self.sync(self._data.close())

    def save(self, dst:str, buffer_size=16384):

        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))

        dst = open(dst, "wb")
        self.reset()
        try:
            shutil.copyfileobj(self.data(), dst, buffer_size)
        finally:
            dst.close()
            self.close()

