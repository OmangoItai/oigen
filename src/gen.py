from .error import OIError
from .types import OIDataType, CppType, Config
from .debug import Debug
from typing import Any, Callable
from pathlib import Path
import subprocess

class OI:

    CPPTypeMap = {
            CppType.Int: int,
            CppType.Float: float,
            CppType.Double: float,
            CppType.Char: str,
            CppType.String: str,
            CppType.Bool: bool,
    }

    def __init__(self, config: dict):
        self.config = Config(
                args=config["args"],
                stdFilePath=Path(config["stdFilePath"]),
                ioFilePath=Path(config["ioFilePath"]),
                dataType=config.get("dataType"),
                timeout=config.get("timeout", 10),
                batch=config.get("batch", 10),
            )
        self.currentBatch = 1
        self.currentMaxBatch = 1
        self.args = {}
        self.handlers = {}
        self._validatePath(self.config.stdFilePath)
        self._validatePathAndCreate(self.config.ioFilePath)
        self.debug = Debug(self)

    def _resolveValue(self, value: Any) -> Any:
        return value() if callable(value) else value

    def _validatePath(self, path: str):
        if not Path(path).exists():
            raise OIError(f"❌️File path invalid: \"{path}\". Plase check out the path.")
    
    def _validatePathAndCreate(self, path: str):
        if not Path(path).exists():
            print(f"❔️File path dose not exist: \"{path}\". Did you want to create it? [y/n]")
            if input().lower() == 'y':
                Path(path).mkdir(parents=True, exist_ok=True)
            else:
                raise OIError(f"❌️File path invalid: \"{path}\". Plase check out the path.")

    def _validateType(self, value: Any, expectedType: CppType) -> bool:
        if callable(value):
            try:
                value = value()
            except Exception as e:
                raise OIError(f"❌️Failed to execute function {value}: {e}.")
        if expectedType == CppType.Char:
            return isinstance(value, str) and len(value) == 1
        return isinstance(value, self.CPPTypeMap[expectedType])
    
    def _validateArgs(self, args: dict[str, Any]) -> None:
        for key, value in args.items():
            if key not in self.config.args:
                raise OIError(f"❌️Unexpected argument \"{key}\". Expected arguments: {list(self.config.args.keys())}.")
            if not self._validateType(value, self.config.args[key]):
                expectedType = self.config.args[key]
                raise OIError(f"❌️Invalid type for \"{key}\", expected {expectedType}({self.CPPTypeMap[expectedType]}) value or function which return this type, but got {type(value)}: {value}.")
    
    def resetCurrentBatch(self):
        self.currentBatch = 1
    
    def setCurrentBatch(self, batch: int):
        self.currentBatch = batch

    def setArgs(self, args: dict[str, Any]):
        self._validateArgs(args)
        self.args = args.copy()
    
    def updateArg(self, args: dict[str, Any]):
        self._validateArgs(args)
        for key, value in args.items():
            self.args[key] = value

    def handler(self, name: str):
        def decorator(func: Callable[..., str]):
            self.handlers[name] = func
            return func
        return decorator
    
    def gen(self, batch: int, handlerName: str):
        for idx in range(self.currentBatch, min(self.config.batch, self.currentBatch + batch - 1) + 1):
            inputFilePath = self.config.ioFilePath / f'{idx}.in'
            outputFilePath = self.config.ioFilePath / f'{idx}.out'
            handler = self.handlers[handlerName]
            resolvedArgs = {key: self._resolveValue(value) for key, value in self.args.items()}
            # gen input
            with open(inputFilePath, 'w') as f:
                f.write(handler(**resolvedArgs))
            # run and gen output
            try:
                with open(inputFilePath, 'r') as stdinFile, open(outputFilePath, 'w') as stdoutFile:
                    result = subprocess.run(
                        [self.config.stdFilePath],
                        stdin=stdinFile,      # 正确传递 stdin
                        stdout=stdoutFile,    # 直接写入文件
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        check=True,
                        timeout=self.config.timeout
                    )
            # 3. error
            except subprocess.CalledProcessError as e:
                if e.returncode == 0xC0000005:
                    raise OIError(f"❌️\"{self.config.stdFilePath}\" crashed with illegal memory access. \n\t❗❗Please check out your STDDD program!😠😠")
                raise OIError(f"❌️Error running \"{self.config.stdFilePath}\":\n\t{e.stderr}") from e
            self.currentBatch += 1
            self.currentMaxBatch = max(self.currentMaxBatch, self.currentBatch)