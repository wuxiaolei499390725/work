from enum import Enum


class LoadPackageType(Enum):
    FromFileSystem = "FromFileSystem"
    FromDtsServer = "FromDtsServer"


class PackageExecutor:
    def __init__(self):
        return
