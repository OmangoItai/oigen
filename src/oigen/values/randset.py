import string, random, sys
from typing import Callable

from oigen.errors import OIError, message

from . import randvar
from ..oitypes import types as oitypes

def randSeq(type: oitypes.CppType, size: int, **kwargs):
    """生成指定类型和长度的随机序列"""
    if type == oitypes.CppType.Int:
        left = kwargs.get('left', -1000)
        right = kwargs.get('right', 1000)
        return [randvar.randInt(left, right)() for _ in range(size)]
    elif type == oitypes.CppType.Float:
        left = kwargs.get('left', -1000.0)
        right = kwargs.get('right', 1000.0)
        return [randvar.randFloat(left, right)() for _ in range(size)]
    elif type == oitypes.CppType.Double:
        left = kwargs.get('left', -1000.0)
        right = kwargs.get('right', 1000.0)
        return [randvar.randDouble(left, right)() for _ in range(size)]
    elif type == oitypes.CppType.Char:
        charset = kwargs.get('charset', string.ascii_letters)
        return [randvar.randChar(charset)() for _ in range(size)]
    elif type == oitypes.CppType.String:
        length = kwargs.get('length', 10)
        charset = kwargs.get('charset', string.ascii_letters + string.digits)
        return [randvar.randString(length, charset)() for _ in range(size)]
    elif type == oitypes.CppType.Bool:
        return [randvar.randBool()() for _ in range(size)]
    else:
        raise OIError(message.TypeError("type", type, oitypes.CppType, "CppType"))