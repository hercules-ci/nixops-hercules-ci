import nixops.statefile
from nixops.locks import LockDriver
from nixops.util import ImmutableValidatedObject
import subprocess
from typing import Optional, List
from nixops_hercules_ci.common import HerculesCICommonBackend, HerculesCICommonBackendOptions
import threading
import time
import json

class HerculesCILockBackendOptions(ImmutableValidatedObject, HerculesCICommonBackendOptions):
    pass

class HerculesCILockBackend(LockDriver[HerculesCILockBackendOptions], HerculesCICommonBackend):
    __options : HerculesCILockBackendOptions
    leaseId : Optional[str]
    pingStopper: Optional[threading.Lock]

    def getOptions(self):
        return self.__options

    @staticmethod
    def options(**kwargs) -> HerculesCILockBackendOptions:
        return HerculesCILockBackendOptions(**kwargs)

    def __init__(self, options: HerculesCILockBackendOptions, **kwargs) -> None:
        self.__options = options
        self.leaseId = None

    def unlock(self, **_kwargs) -> None:
        if self.leaseId is not None:
            r = self.runHci(["lock", "release", "--lease-id", self.leaseId])
        self.leaseId = None
        if self.pingStopper is not None:
            self.pingStopper.release()
        self.pingStopper = None

    def _ping(self) -> None:
        if self.leaseId is not None:
            r = self.runHci(["lock", "update", "--lease-id", self.leaseId] + self.getProjectArgs())

    # NB: description and exclusive aren't actually part of the NixOps interface yet.
    def lock(self, description="NixOps", exclusive=True, **_kwargs) -> None:
        if self.leaseId is not None:
            raise Exception("A lock has already been taken! Hercules CI supports recursive locking, but provisions need to be made for it in the NixOps locking interface. It is unsupported for now. Most likely the double locking is due to a programming error in NixOps.")

        if exclusive:
            exclusiveFlag = []
        else:
            exclusiveFlag = ["--non-exclusive"]

        r = self.runHci(["lock", "acquire", "--description", description, "--json"] + exclusiveFlag + self.getArgs(), stdout=subprocess.PIPE)
        resp = json.loads(r.stdout)

        self.leaseId = resp["leaseId"]
        self.pingStopper = threading.Lock()
        self.pingStopper.acquire()

        def pinger():
            while self.leaseId is not None and self.pingStopper is not None and self.pingStopper.acquire(blocking=True, timeout=3*60) == False:
                self._ping()

        t = threading.Thread(target=pinger)
        t.start()
