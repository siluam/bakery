let
    name = "20220208045251813793805";
    pkgs = import <nixpkgs> {};
    venv = "~/.local/nix-shells/${name}/venv";
in (pkgs.mkShell rec {
    inherit name;
    buildInputs = with pkgs; [ python310 gcc ];
    nativeBuildInputs = buildInputs;
    shellHook = ''
        python3 -m venv ${venv}
        source ${venv}/bin/activate
        pip install --upgrade pip || :
        pip install . \
                    coconut \
                    cytoolz \
                    xonsh || :
        exec xonsh
    '';
})
