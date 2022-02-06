let
    name = "bakery";
in with import <nixpkgs> {};
stdenv.mkDerivation rec {
  inherit name;
  buildInputs = with pkgs; [ python310 gcc ];
  nativeBuildInputs = buildInputs;
  shellHook = ''
    python3 -m venv ~/.local/${name}
    source ~/.local/${name}/bin/activate
    pip install https://github.com/shadowrylander/bakery/archive/main.tar.gz \
                coconut \
                cytoolz \
                xonsh || :
    exec xonsh
  '';
}
