from pathlib import Path
from typing import Any, Optional
import sys

from rich.console import Console
from rich.traceback import install
install(show_locals=True)

class OIError(Exception):
    def __init__(self, message):
        self.message = message.strip()
        self.message = '\n\t\t'.join(self.message.split('\n'))
        super().__init__(self.message)
    def __str__(self):
        return self.message

def OIExcepthook(exc_type, exc_value, exc_traceback):
    console = Console(stderr=True)
    tb = exc_traceback
    first = None
    while tb:
        first = tb  # 记录第一个 traceback
        last = tb  # 记录最后一个 traceback
        tb = tb.tb_next

    if first and last:
        first_lineno = first.tb_lineno
        first_filename = first.tb_frame.f_code.co_filename

        console.print(f"\t⚠️  [bold white on bright_yellow]Error at:[/] [bright_green]{first_filename}:{first_lineno}\n")
        console.print(f"\t❌ [bold white on red]{exc_type.__name__}[/]: [bold bright_white]{exc_value}\n")



sys.excepthook = OIExcepthook

class message:
    @staticmethod
    def runtimeError(path: str|Path, e: Optional[str] = None):
        msg = f"Error running \"{path}\""
        if e:
            msg += f"\n{e}"
        return msg
    
    @staticmethod
    def MemoryInvalid(path: str|Path, e: Optional[Any] = None):
        msg = f"\"{path}\" crashed with illegal memory access. \n❗❗Please check out your STDDDDDD program!😠😠"
        if e:
            msg += f"\n{e}"
        return msg
    
    @staticmethod
    def TypeError(key: Any, value: Any, expectedType: Any, expectedTypedesc: Any, e: Optional[Any] = None):
        msg = f"Invalid type for \"{key}\", expected {expectedType}({expectedTypedesc}) value or function which return this type, but got {type(value)}: {value}."
        if e:
            msg += f"\n{e}"
        return msg

    @staticmethod
    def ConfigArgumentsInvalid(key: Any, args: Any, e: Optional[Any] = None):
        msg =  f"Unexpected argument \"{key}\". Expected arguments: {args}."
        if e:
            msg += f"\n{e}"
        return msg
    
    @staticmethod
    def ValueError(value: Any, e: Optional[Any] = None):
        msg = f"Failed to extract value on function {value}"
        if e:
            msg += f"\n{e}"
        return msg
    
    @staticmethod
    def PathError(path: str|Path, e: Optional[Any] = None):
        msg = f"Path invalid: \"{path}\".\nPlease check out the path."
        if e:
            msg += f"\n{e}"
        return msg
    
    @staticmethod
    def RangeInvalid(left: Any, right: Any, e: Optional[Any] = None):
        msg = f"Invalid range :({left}, rightLimit:{right}).\n❗❗Please check out the range!😠😠"
        if e:
            msg += f"\n{e}"
        return msg