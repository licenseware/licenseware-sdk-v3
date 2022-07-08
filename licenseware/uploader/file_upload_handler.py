import os
import io
import shutil
from typing import Union, IO


class FileUploadHandler:

    def __init__(self, fileorbuffer: Union[str, IO]) -> None:

        self.fileorbuffer = fileorbuffer
        self.filename = None
        self.buffer = None
        if isinstance(self.fileorbuffer, str):
            if not os.path.isfile(self.fileorbuffer):
                raise FileNotFoundError(f"File {self.fileorbuffer} was not found on disk")

        if isinstance(self.fileorbuffer, str):
            self.buffer = open(self.fileorbuffer, "rb") 
            self.filename = os.path.basename(self.fileorbuffer)
        else:
            
            # All attrs
            # attrs = ['close', 'closed', 'detach', 'fileno', 'flush', 'isatty', 'mode', 
            # 'name', 'peek', 'raw', 'read', 'read1', 'readable', 'readinto', 
            # 'readinto1', 'readline', 'readlines', 'seek', 'seekable', 'tell', 
            # 'truncate', 'writable', 'write', 'writelines']

            # Mandatory attrs
            attrs = ['close', 'flush', 'mode', 
            'raw', 'read', 'readline', 'readlines', 'seek', 'tell', 
            'write', 'writelines']
            
            for name, val in vars(self.fileorbuffer).items():
                if isinstance(val, io.BytesIO) and all(hasattr(val, attr) for attr in attrs) and self.buffer is None:
                    self.buffer = val
                if name in ["filename", "name"] and self.filename is None:
                    self.filename = val
                    
            if self.buffer is None:
                raise AttributeError(f"Mandatory attributes '{', '.join(attrs)}' not found on provided BytesIO object.")
            
            if self.filename is None:
                raise AttributeError("Can't find `filename` for this file")

    
    def reset(self):
        return self.buffer.seek(0) 

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

    # Except `reset` and `save` methods the rest just proxy request to buffer class
    # Tried different ways to avoid this with: 
    # __new__, setattr, cls1.__dict__.update(cls2.__dict__)
    # but they didn't work

    # Proxy calls
    
    def writelines(self, __lines):
        return self.buffer.writelines(__lines)

    def writable(self):
        return self.buffer.writable()

    def write(self, __buffer):
        return self.buffer.write(__buffer)

    def truncate(self, __size):
        return self.buffer.truncate(__size)

    def tell(self):
        return self.buffer.tell()

    def seekable(self):
        return self.buffer.seekable()

    def seek(self, __offset:int, __whence:int):
        return self.buffer.seek(__offset, __whence)

    def readlines(self, __hint):
        return self.buffer.readlines(__hint)

    def readline(self, __size):
        return self.buffer.readline(__size)

    def readinto1(self, __buffer):
        return self.buffer.readinto1(__buffer)

    def readinto(self, __buffer):
        return self.buffer.readinto(__buffer)

    def readable(self):
        return self.buffer.readable()

    def read1(self, __size: int = ...):
        return self.buffer.read1(__size)

    def read(self, __size: int = ...):
        return self.buffer.read(__size)

    @property
    def raw(self):
        return self.buffer.raw

    def peek(self, __size: int = ...):
        return self.buffer.peek(__size)

    @property
    def name(self):
        return self.buffer.name

    @property
    def mode(self):
        return self.buffer.mode

    def isatty(self):
        return self.buffer.isatty()

    def flush(self):
        return self.buffer.flush()

    def fileno(self):
        return self.buffer.fileno()

    def detach(self):
        return self.buffer.detach()

    @property
    def closed(self):
        return self.buffer.closed

    def close(self):
        return self.buffer.close()


