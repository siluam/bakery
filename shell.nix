{ pkgs ? import <nixpkgs> {} }:

let
  mach-nix = import (
    builtins.fetchGit {
      url = "https://github.com/DavHau/mach-nix/";
      ref = "master";
    }
  );
  customPython = mach-nix.mkPython {
    python = pkgs.python38;
    requirements = '' pip '';
  };
in pkgs.mkShell {
  buildInputs = [ customPython ];
}
