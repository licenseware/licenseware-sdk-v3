import os
import io
import shutil
from typing import Union, IO



class FileUploadHandler:

    def __init__(self, fileorbuffer: Union[str, IO]) -> None:
        self.fileorbuffer = fileorbuffer
        self.filename = None
        self._data = None
        if isinstance(self.fileorbuffer, str):
            if not os.path.isfile(self.fileorbuffer):
                raise FileNotFoundError(f"File {self.fileorbuffer} was not found on disk")

        if isinstance(self.fileorbuffer, str):
            self._data = open(self.fileorbuffer, "rb") 
            self.filename = os.path.basename(self.fileorbuffer)
        else:
            
            attrs = ["read", "seek", "close", "tell", "seekable"]
            
            for name, val in vars(self.fileorbuffer).items():
                if isinstance(val, io.BytesIO) and all(hasattr(val, attr) for attr in attrs) and self._data is None:
                    self._data = val
                if name in ["filename", "name"] and self.filename is None:
                    self.filename = val
                    
            if self._data is None:
                raise AttributeError(f"Mandatory attributes '{', '.join(attrs)}' not found on provided BytesIO object.")
            
            if self.filename is None:
                raise AttributeError("Can't find `filename` for this file")


    def __call__(self):
        return self

    def read(self, buffering: int = None) -> bytes:
        return self._data.read(buffering)

    def seek(self, offset: int, whence: int = 0) -> int:
        return self._data.seek(offset, whence)
        
    def tell(self):
        return self._data.tell()

    def seekable(self):
        return self._data.seekable()

    def reset(self):
        return self._data.seek(0) 

    def close(self):
        self._data.close()

    def save(self, dst:str, buffer_size=16384):

        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))

        dst = open(dst, "wb")
        self.reset()
        try:
            shutil.copyfileobj(self, dst, buffer_size)
        finally:
            dst.close()
            self.close()

