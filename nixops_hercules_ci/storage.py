import nixops.statefile
from nixops.storage import StorageBackend
from nixops.util import ImmutableValidatedObject
import subprocess
from typing import Optional, List
from nixops_hercules_ci.common import HerculesCICommonBackend, HerculesCICommonBackendOptions

class HerculesCIStorageBackendOptions(ImmutableValidatedObject, HerculesCICommonBackendOptions):
    pass

class HerculesCIStorageBackend(StorageBackend[HerculesCIStorageBackendOptions], HerculesCICommonBackend):
    __options : HerculesCIStorageBackendOptions
    def getOptions(self):
        return self.__options

    @staticmethod
    def options(**kwargs) -> HerculesCIStorageBackendOptions:
        return HerculesCIStorageBackendOptions(**kwargs)

    def __init__(self, options: HerculesCIStorageBackendOptions, **kwargs) -> None:
        self.__options = options

    def fetchToFile(self, path: str, **kwargs) -> None:
        self.runHci(["state", "get", "--file", path] + self.getArgs())

    def uploadFromFile(self, path: str, **kwargs) -> None:
        self.runHci(["state", "put", "--file", path] + self.getArgs())
