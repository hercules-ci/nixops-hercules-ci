import nixops.statefile
from nixops.locks import LockDriver
from nixops.util import ImmutableValidatedObject
import subprocess
from typing import Optional, List
from nixops_hercules_ci.common import HerculesCICommonBackend, HerculesCICommonBackendOptions
import time

class HerculesCILockBackendOptions(ImmutableValidatedObject, HerculesCICommonBackendOptions):
    pass

class HerculesCILockBackend(LockDriver[HerculesCILockBackendOptions], HerculesCICommonBackend):
    __options : HerculesCILockBackendOptions
    def getOptions(self):
        return self.__options

    @staticmethod
    def options(**kwargs) -> HerculesCILockBackendOptions:
        return HerculesCILockBackendOptions(**kwargs)

    def __init__(self, options: HerculesCILockBackendOptions, **kwargs) -> None:
        self.__options = options

    def unlock(self, **_kwargs) -> None:
        # TBD
        pass

    def lock(self, **_kwargs) -> None:
        # TBD
        pass
