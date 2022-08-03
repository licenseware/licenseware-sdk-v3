import io
import os
import shutil
import tempfile
from typing import IO, Union


class FileUploadHandler(io.BufferedIOBase):
    def __init__(self, fileorbuffer: Union[str, IO]) -> None:
        self.fileorbuffer = fileorbuffer
        self.filename = None
        self.buffer = None
        if isinstance(self.fileorbuffer, str):
            if not os.path.isfile(self.fileorbuffer):
                raise FileNotFoundError(
                    f"File {self.fileorbuffer} was not found on disk"
                )  # pragma: no cover

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
            attrs = ["close", "read", "seek", "tell", "write"]

            for name, val in vars(self.fileorbuffer).items():
                if (
                    isinstance(
                        val,
                        (
                            tempfile.SpooledTemporaryFile,
                            io.BytesIO,
                        ),
                    )
                    and all(hasattr(val, attr) for attr in attrs)
                    and self.buffer is None
                ):
                    self.buffer = val

                if name in ["filename", "name"] and self.filename is None:
                    self.filename = val

            if self.buffer is None:
                raise AttributeError(
                    f"Mandatory attributes '{', '.join(attrs)}' not found on provided BytesIO object."
                )  # pragma: no cover

            if self.filename is None:
                raise AttributeError(
                    "Can't find `filename` for this file"
                )  # pragma: no cover

    def reset(self):
        return self.buffer.seek(0)

    def save(self, dst: str, buffer_size=16384):

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

    def writelines(self, __lines=None):
        return self.buffer.writelines(__lines)  # pragma: no cover

    def writable(self):
        return self.buffer.writable()  # pragma: no cover

    def write(self, __buffer=None):
        return self.buffer.write(__buffer)  # pragma: no cover

    def truncate(self, __size=None):
        return self.buffer.truncate(__size)  # pragma: no cover

    def tell(self):
        return self.buffer.tell()  # pragma: no cover

    def seekable(self):
        return self.buffer.seekable()  # pragma: no cover

    def seek(self, __offset: int, __whence: int = 0):
        return self.buffer.seek(__offset, __whence)  # pragma: no cover

    def readlines(self, __hint=None):
        return self.buffer.readlines(__hint)  # pragma: no cover

    def readline(self, __size=None):
        return self.buffer.readline(__size)  # pragma: no cover

    def readinto1(self, __buffer=None):
        return self.buffer.readinto1(__buffer)  # pragma: no cover

    def readinto(self, __buffer=None):
        return self.buffer.readinto(__buffer)  # pragma: no cover

    def readable(self):
        return self.buffer.readable()  # pragma: no cover

    def read1(self, __size: int = None):
        return self.buffer.read1(__size)  # pragma: no cover

    def read(self, __size: int = None):
        return self.buffer.read(__size)  # pragma: no cover

    @property
    def raw(self):
        return self.buffer.raw  # pragma: no cover

    def peek(self, __size: int = None):
        return self.buffer.peek(__size)  # pragma: no cover

    @property
    def name(self):
        return self.buffer.name  # pragma: no cover

    @property
    def mode(self):
        return self.buffer.mode  # pragma: no cover

    def isatty(self):
        return self.buffer.isatty()  # pragma: no cover

    def flush(self):
        return self.buffer.flush()  # pragma: no cover

    def fileno(self):
        return self.buffer.fileno()  # pragma: no cover

    def detach(self):
        return self.buffer.detach()  # pragma: no cover

    @property
    def closed(self):
        return self.buffer.closed  # pragma: no cover

    def close(self):
        return self.buffer.close()  # pragma: no cover
