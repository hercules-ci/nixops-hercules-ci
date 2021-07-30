from nixops.storage import StorageBackend

from nixops_hercules_ci.storage import HerculesCIStorageBackend
from nixops_hercules_ci.lock import HerculesCILockBackend
import nixops.plugins
from nixops.locks import LockDriver
from typing import Dict, Type

class HerculesCIPlugin(nixops.plugins.Plugin):
    def storage_backends(self) -> Dict[str, Type[StorageBackend]]:
        return {"hercules-ci": HerculesCIStorageBackend}

    def lock_drivers(self) -> Dict[str, Type[LockDriver]]:
        return {"hercules-ci": HerculesCILockBackend}

@nixops.plugins.hookimpl
def plugin():
    return HerculesCIPlugin()
