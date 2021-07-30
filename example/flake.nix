{
  description = "example";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils, ... }:
    let
      pkgsFor = system: import nixpkgs {
        inherit system;
        overlays = [ self.overlay ];
      };

    in
    {
      overlay = final: prev: {
        blog = prev.callPackage ./blog { };
      };

      nixopsConfigurations.default = {
        inherit nixpkgs;
        network.description = "example";
        network.storage.hercules-ci = {
          stateName = "foo";
        };
        # !!! Locking not implemented yet
        network.lock.hercules-ci = {
          stateName = "foo";
        };
        defaults.nixpkgs.pkgs = pkgsFor "x86_64-linux";
      };

    } // utils.lib.eachDefaultSystem (system:
      let pkgs = pkgsFor system;
      in
      {
        devShell = pkgs.mkShell {
          nativeBuildInputs = [
          ];
        };
      }
    );
}
