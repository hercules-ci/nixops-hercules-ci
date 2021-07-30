{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-21.05";
    flake-compat.url = "github:edolstra/flake-compat";
    flake-compat.flake = false;
  };

  outputs = { self, nixpkgs, ... }: {

    checks.x86_64-linux.build = import ./default.nix { pkgs = nixpkgs.legacyPackages.x86_64-linux; };

  };
}
