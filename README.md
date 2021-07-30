
# NixOps Hercules CI plugin

This lets you use Hercules CI state files as a backend for NixOps state.
Some benefits:

 - Centralized: no more outdated state accidents
 - Records state version history remotely
 - Reuses hci credentials
 - Links state versions to GitHub users
 - Low configuration: only a remote file name

## Status

Currently experimental because of the following:

  - [ ] NixOps state storage api release (NixOps 2.0)
    - [ ] Decide on [fine-grained](https://github.com/NixOS/nixops/pull/1264#issuecomment-889884626) state storage
  - [ ] Implement locking (besides the implicit effect ordering on CI)

## Usage

Add to your NixOps network expression:

```nix
network.storage.hercules-ci = {
  stateName = "storage.nixops";
};
```

Add to your devShell, if you haven't already:

```
nativeBuildInputs = [ pkgs.hci ];
```

You can now create a new deployment or migrate an existing one.

## Create a new deployment

TODO

## Migrate an existing deployment

TODO

## Hacking

```shell
nix-shell
poetry install
poetry shell
```