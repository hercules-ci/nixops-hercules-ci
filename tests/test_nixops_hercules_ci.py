
from nixops_hercules_ci.storage import HerculesCIStorageBackend

def test_args_1():
    backend = HerculesCIStorageBackend(HerculesCIStorageBackend.options(stateName = 'foo'))
    assert backend.getArgs() == ["--name", "foo"]

def test_args_2():
    backend = HerculesCIStorageBackend(HerculesCIStorageBackend.options(stateName = 'foo', project = 'x/y/z'))
    assert backend.getArgs() == ["--name", "foo", "--project", "x/y/z"]
