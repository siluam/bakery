let
    name = "4d28e002-8dfd-41d5-a4af-1aa20f7f99ea";
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
