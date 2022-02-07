let
    name = "bakery";
    pkgs = import <nixpkgs> {};
in (pkgs.buildFHSUserEnv {
    inherit name;
    targetPkgs = pkgs: with pkgs; [ python310 gcc ];
    runScript = ''
        pip install --upgrade pip
        pip install . \
                    coconut \
                    cytoolz \
                    xonsh || :
        exec xonsh
    '';
}).env
