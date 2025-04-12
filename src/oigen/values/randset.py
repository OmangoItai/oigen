import string, random, sys
from typing import Callable

from oigen.errors import OIError, message

import randvar
import oitypes

def randSeq(type: oitypes.CppType, size: int, ):
    if type == oitypes.CppType.Int:
        return [randvar.randInt() for _ in range(size)]
    elif type == oitypes.CppType.Float:
    elif type == oitypes.CppType.Double:
    elif type == oitypes.CppType.Char:
    elif type == oitypes.CppType.String:
    elif type == oitypes.CppType.Bool: