
# NixOps Hercules CI plugin

This lets you use Hercules CI state files as a backend for NixOps state.
Some benefits:

 - Centralized: no more outdated state accidents
 - Records state version history remotely
 - Reuses hci credentials
 - Links state versions to GitHub users or CI jobs
 - Low configuration: only a remote file name
 - Locking support, including read-only/rw distinction
 - CI can pre-build the network
 - CI/CD agent does not need to idle while waiting for lock because
   the (cloud) coordinator is aware of the lock _(planned feature)_
 - Clearly communicates why it's waiting for a lock

## Status

Currently experimental because of the following:

  - [ ] NixOps state storage api release (NixOps 2.0)
    - [x] Decide on [fine-grained](https://github.com/NixOS/nixops/pull/1264#issuecomment-889884626) state storage -> not feasible at this time; choose unique `stateName`s
  - [x] Implement locking (besides the implicit effect ordering on CI)
  - [ ] Upstream improvements to locking
    - [ ] Fix known_hosts handling: https://github.com/NixOS/nixops/pull/1464
    - [ ] Improve locking for real world use https://github.com/NixOS/nixops/pull/1470

A module and resource for retrieving secrets will be added.

## Usage

Add to your NixOps network expression:

```nix
network.storage.hercules-ci = {
  stateName = "default.nixops";
};
network.lock.hercules-ci = {
  stateName = "default.nixops";
};
```

Add to your devShell, if you haven't already:

```
nativeBuildInputs = [ pkgs.hci ];
```

You can now create a new deployment or migrate an existing one.

## Create a new deployment

1. Add your repository to Hercules CI.

2. Create an empty state file

   ```
   hci state put --name default.nixops --file /dev/null
   ```

3. Set a unique `stateName` in the storage backend and lock backend.

   Note: While it's possible to create more than one deployment in a single
   state file, this is not recommended because operations on one deployment
   will block the others.

4. Initialize the state file with a deployment

   ```
   nixops create
   ```

5. Deploy

   ```
   nixops deploy
   ```

## Migrate an existing deployment

1. Export the state to a file using the legacy storage backend.

   ```
   nixops export -d my-deployment >tmp.nixops
   ```

2. Change the storage backend and lock backend to `hercules-ci`, choosing a unique `stateName` for the deployment.

   Note: While it's possible to have more than one deployment in a single
   state file, this is not recommended because operations on one deployment
   will block the others.

3. Import from the file.

   ```
   nixops import <tmp.nixops
   ```

4. Remove the file. It may contain sensitive values.

   ```
   rm tmp.nixops
   ```

## Attributes

### `network.storage.hercules-ci`

`stateName`: Required string attribute that identifies the state file; `--name` in `hci`. State files are visible in the dashboard. Go to a repo and click the State tab.

`project`: Optional string attribute identifying the repository, consisting of the site (`github`), owner and repo name, separated by slashes `/`. Example: `github/hercules-ci/hercules-ci-agent`. Defaults to the upstream of the current branch when unset.

### `network.lock.hercules-ci`

`stateName`: Required string attribute that identifies the lock; this is intentionally the same as the storage key, but their relation is not enforced.

`project`: Optional string attribute identifying the repository, consisting of the site (`github`), owner and repo name, separated by slashes `/`. Example: `github/hercules-ci/hercules-ci-agent`. Defaults to the upstream of the current branch when unset.


## Hacking

```shell
nix-shell
poetry install
poetry shell
```
