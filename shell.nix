{ pkgs ? import <nixpkgs> { } }:
let
  overrides = import ./overrides.nix { inherit pkgs; };
in
pkgs.mkShell {
  nativeBuildInputs = [ pkgs.nixpkgs-fmt pkgs.poetry ];
  buildInputs = [
    (pkgs.poetry2nix.mkPoetryEnv {
      projectDir = ./.;
      overrides = pkgs.poetry2nix.overrides.withDefaults overrides;
    })
    pkgs.poetry
  ];
}
