from typing import Dict
from pathlib import Path
from enum import Enum
from dataclasses import dataclass

class OIDataType(Enum):
    Sequence = 1
    Matrix = 2
    Graph = 3

class CppType(Enum):
    Int = 1
    Float = 2
    Double = 3
    Char = 4
    String = 5
    Bool = 6

@dataclass
class Config:
    args: Dict[str, CppType]
    stdFilePath: Path
    ioFilePath: Path
    dataType: OIDataType = None
    timeout: int = 10
    batch: int = 10

    def __post_init__(self):
        self.stdFilePath = self.stdFilePath.absolute()
        self.ioFilePath = self.ioFilePath.absolute()
