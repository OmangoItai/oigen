from typing import Any, Callable, Optional
from pathlib import Path
import subprocess

from InquirerPy import inquirer
from rich.console import Console
from rich.progress import Progress
console = Console()

from .errors import OIError, message
from .oitypes import CppType, Config
from .debug import Debug

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
            raise OIError(message.PathError(path))
    
    def _validatePathAndCreate(self, path: str):
        if not Path(path).exists():
            console.print(f"❔[bold blue]File path does not exist:[/] [yellow]\"{path}\"[/]")
            choice = inquirer.select(
                message="  Do you wanna create one?\n",
                choices=["📂 Create", "❌ Cancel"],
                default="📂 Create",
            ).execute()
            if choice == "📂 Create":
                Path(path).mkdir(parents=True, exist_ok=True)
                console.print(f"✅ [green]{Path(path).absolute()}[/] created.")
            else:
                raise OIError(message.PathError(path))

    def _validateType(self, value: Any, expectedType: CppType) -> bool:
        if callable(value):
            try:
                value = value()
            except Exception as e:
                raise OIError(message.ValueError(value, e)) from e
        if expectedType == CppType.Char:
            return isinstance(value, str) and len(value) == 1
        return isinstance(value, self.CPPTypeMap[expectedType])
    
    def _validateArgs(self, args: dict[str, Any]) -> None:
        for key, value in args.items():
            if key not in self.config.args:
                raise OIError(message.ConfigArgumentsInvalid(key, list(self.config.args.keys())))
            if not self._validateType(value, self.config.args[key]):
                expectedType = self.config.args[key]
                raise OIError(message.TypeError(key, value, expectedType, expectedTypedesc = self.CPPTypeMap[expectedType]))
    
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
    
    def gen(self, batch: int, handlerName: str, args: Optional[dict[str, Any]] = None):
        if args:
            self.setArgs(args)
        with Progress() as progress:
            targetBatches = min(self.config.batch, self.currentBatch + batch - 1) + 1
            task = progress.add_task("[cyan]Gnerating...", total = targetBatches - self.currentBatch)
            for idx in range(self.currentBatch, targetBatches):
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
                        raise OIError(message.MemoryInvalid(self.config.stdFilePath), e) from e
                    raise OIError(message.runtimeError(self.config.stdFilePath, e)) from e
                progress.update(task, advance=1)
                progress.refresh()
                progress.console.log(f"\"{inputFilePath.name}\", \"{outputFilePath.name}\" [bold green]done.[/]")
                self.currentBatch += 1
                self.currentMaxBatch = max(self.currentMaxBatch, self.currentBatch)
