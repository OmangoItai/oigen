import string, random, sys
from ..src.error import OIError
from typing import Callable

maxInt = sys.maxsize
minInt = -sys.maxsize - 1
minFloat = -1e10
maxFloat = 1e10
minDouble = -sys.float_info.max / 10  # 避免溢出
maxDouble = sys.float_info.max / 10
alphabet = string.ascii_letters  # 默认字符集（大小写字母）

@staticmethod
def _validateLimit(left: int, right: int):
    if left > right:
        raise OIError(f"❌️Invalid range leftLimit:{left} > rightLimit:{right}.\n❗❗Please check out the range!😠😠")

@staticmethod
def randInt(left: int = minInt, right: int = maxInt) -> Callable[[int, int], int]:
    _validateLimit(left, right)
    def _(left: int = left, right: int = right) -> int:
        return random.randint(left, right)
    return _

@staticmethod
def randFloat(left: float = minFloat, right: float = maxFloat) -> Callable[[float, float], float]:
    _validateLimit(left, right)
    def _(left: float = left, right: float = right) -> float:
        return random.uniform(left, right)
    return _

@staticmethod
def randDouble(left: float = minDouble, right: float = maxDouble) -> Callable[[float, float], float]:
    _validateLimit(left, right)
    def _(left: float = left, right: float = right) -> float:
        return random.uniform(left, right)
    return _

@staticmethod
def randChar(charset: str = alphabet) -> Callable[[], str]:
    def _(charset: str = charset) -> str:
        return random.choice(charset)
    return _

@staticmethod
def randString(length: int = 10, charset: str = alphabet + string.digits) -> Callable[[], str]:
    def _(length: int = length, charset: str = charset) -> str:
        return ''.join(random.choices(charset, k=length))
    return _

@staticmethod
def randBool() -> Callable[[], bool]:
    def _() -> bool:
        return random.choice([True, False])
    return _