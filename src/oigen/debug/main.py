from pathlib import Path
from typing import List
import subprocess

from oigen.errors import OIError

class Debug:
    def __init__(self, oiInstance):
        self.oi = oiInstance
    
    def run(self,targetBatches: List[int] = [], printOnly: bool = False):
        if not targetBatches:
            targetBatches = range(1, self.oi.currentMaxBatch + 1)
        targetPaths = [self.oi.config.ioFilePath / f"{tb}.in" for tb in targetBatches]
        for filename in targetPaths:
            inputFilePath = self.oi.config.ioFilePath / filename
            outputFilePath = self.oi.config.ioFilePath / filename.replace(".in", ".out")

            with open(inputFilePath, 'r') as stdinFile:
                if printOnly:
                    result = subprocess.run(
                        [self.oi.config.stdFilePath],
                        stdin=stdinFile,
                        stdout=subprocess.PIPE,  # 捕获输出
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        check=True,
                        timeout=self.oi.config.timeout
                    )
                    print(f"=== Output for {filename} ===")
                    print(result.stdout)
                    print("=" * 30)
                else:
                    with open(outputFilePath, 'w') as stdoutFile:
                        result = subprocess.run(
                            [self.oi.config.stdFilePath],
                            stdin=stdinFile,
                            stdout=stdoutFile,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            check=True,
                            timeout=self.oi.config.timeout
                        )

            if result.stderr:
                raise OIError(f"❌️Error in running {self.oi.config.stdFilePath} on {filename}:\n\t{result.stderr}.")
    
    def compareRun(self, otherPath: Path | str, targetBatches: List[int] = [], isPrint: bool = False):
        failedMatches = []
        otherPath = Path(otherPath)
        if not targetBatches:
            targetBatches = range(1, self.oi.currentMaxBatch + 1)
        targetPaths = [self.oi.config.ioFilePath / f"{tb}.in" for tb in targetBatches]
        for filename in targetPaths:
            inputFilePath = self.oi.config.ioFilePath / filename

            # stdFilePath
            with open(inputFilePath, 'r') as stdinFile:
                stdResult = subprocess.run(
                    [self.oi.config.stdFilePath],
                    stdin=stdinFile,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    check=True,
                    timeout=self.oi.config.timeout
                )

            if stdResult.stderr:
                raise OIError(f"❌️Error in running {self.oi.config.stdFilePath} on {filename}:\n\t{stdResult.stderr}.")

            # otherPath
            with open(inputFilePath, 'r') as stdinFile:
                otherResult = subprocess.run(
                    [otherPath],
                    stdin=stdinFile,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    check=True,
                    timeout=self.oi.config.timeout
                )

            if otherResult.stderr:
                raise OIError(f"❌️Error in running {otherPath} on {filename}:\n\t{otherResult.stderr}.")

            # compare
            if stdResult.stdout.strip() != otherResult.stdout.strip():
                failedMatches.append(filename)
                if isPrint:
                    l = (30 - len(filename.name)) // 2
                    r = 30 - l
                    print('='*l, filename.name, '='*r)
                    print(f"{self.oi.config.stdFilePath.name}:\n{stdResult.stdout}")
                    print(f"{otherPath.name}:\n{otherResult.stdout}")

        return True if not failedMatches else failedMatches