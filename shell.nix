{ pkgs, lib ? pkgs.lib }:

let
  ppython = "python3.8";
  python = builtins.replaceStrings ["."] [""] ppython;
  mach-nix = import (
    builtins.fetchGit {
      url = "https://github.com/DavHau/mach-nix/";
      ref = "master";
    }
  ) { inherit python pkgs; };
  customPython = mach-nix.mkPython { requirements = ''  ''; };
in pkgs.mkShell {
  buildInputs = [ customPython ] ++ (with pkgs."${python}Packages"; [ pip setuptools ]);
  shellHook = ''
    alias pip="PIP_PREFIX='$(pwd)/_build/pip_packages' \pip"
    export PYTHONPATH="$(pwd)/_build/pip_packages/lib/${ppython}/site-packages:$PYTHONPATH"
    unset SOURCE_DATE_EPOCH
  '';
}
