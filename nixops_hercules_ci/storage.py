import nixops.statefile
from nixops.storage import StorageBackend
from nixops.util import ImmutableValidatedObject
import subprocess
from typing import Optional, List
from nixops_hercules_ci.common import HerculesCICommonBackend, HerculesCICommonBackendOptions
import json
from typing import (Dict, Any)
import os
import sys
import hashlib

class HerculesCIStorageBackendOptions(ImmutableValidatedObject, HerculesCICommonBackendOptions):
    pass

class HerculesCIStorageBackend(StorageBackend[HerculesCIStorageBackendOptions], HerculesCICommonBackend):
    __options : HerculesCIStorageBackendOptions

    importJson : Optional[Dict[str, Any]]
    fetchedHash : Optional[bytes]

    def getOptions(self):
        return self.__options

    @staticmethod
    def options(**kwargs) -> HerculesCIStorageBackendOptions:
        return HerculesCIStorageBackendOptions(**kwargs)

    def __init__(self, options: HerculesCIStorageBackendOptions, **kwargs) -> None:
        self.__options = options

    def fetchToFile(self, path: str, **kwargs) -> None:
        self.runHci(["state", "get", "--file", path] + self.getArgs())
        self.fetchedHash = self.hashFile(path)

        # If we're dealing with an export, we remove the file so NixOps can 
        # initialize it, and hold onto the json.
        try:
            with open(path, "rb") as fileHandle:
                self.importJson = json.load(fileHandle)
                sys.stderr.write("The remote state was in NixOps export format. It will be migrated to NixOps database format.\n")
            os.remove(path)
        except ValueError:
            self.importJson = None
            pass

    def uploadFromFile(self, path: str, **kwargs) -> None:
        newHash = self.hashFile(path)
        if newHash is not self.fetchedHash:
            sys.stderr.write("nixops state file updated; uploading...\n")
            self.runHci(["state", "put", "--file", path] + self.getArgs())
        else:
            sys.stderr.write("nixops state file unaltered.\n")

        fetchedHash = newHash

    def onOpen(self, sf: nixops.statefile.StateFile, **kwargs) -> None:
        existing_deployments = set(sf.query_deployments())
        if self.importJson is not None:
            for uuid, attrs in self.importJson.items():
                if uuid in existing_deployments:
                    raise Exception(
                        "state was expected to be empty, but already contained a deployment with UUID {0}".format(uuid)
                    )
                with sf._db:
                    depl = sf.create_deployment(uuid=uuid)
                    depl.import_(attrs)

    @staticmethod
    def hashFile(path: str) -> bytes:
        sha256 = hashlib.sha256()
        with open(path, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                sha256.update(data)
        return sha256.digest()
