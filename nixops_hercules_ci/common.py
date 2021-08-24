import nixops.statefile
from typing import Optional, List
import subprocess
from abc import abstractmethod

'''
Common options for the lock and storage backends.
'''
class HerculesCICommonBackendOptions():
    stateName : str
    project : Optional[str]

'''
Common logic for the lock and storage backends.
'''
class HerculesCICommonBackend():
    def getOptions(self) -> HerculesCICommonBackendOptions:
        raise NotImplementedError("subclass must implement getOptions")

    def getArgs(self) -> List[str]:
        options = self.getOptions()
        return ["--name", options.stateName] + self.getProjectArgs()

    def getProjectArgs(self) -> List[str]:
        options = self.getOptions()
        if options.project is not None:
            return ["--project", options.project]
        else:
            return []

    def runHci(self, args, **kwargs) -> subprocess.CompletedProcess:
        hciExePath = "hci"
        try:
            return subprocess.run([hciExePath] + args, check=True, **kwargs)
        except FileNotFoundError:
            # TODO a stack trace would be redundant. Try to avoid it.
            raise Exception("Could not find the 'hci' executable on PATH. The NixOps Hercules CI plugin needs this command. You can get it from Nixpkgs: pkgs.hci")
