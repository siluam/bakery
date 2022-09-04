{
    description = "An \"sh\" alternative!";
    inputs = rec {
        settings.url = github:sylvorg/settings;
        titan.url = github:syvlorg/titan;
        py3pkg-oreo.url = github:syvlorg/oreo;
        py3pkg-pytest-hy.url = github:syvlorg/pytest-hy;
        flake-utils.url = github:numtide/flake-utils;
        flake-compat = {
            url = "github:edolstra/flake-compat";
            flake = false;
        };
    };
    outputs = inputs@{ self, flake-utils, settings, ... }: with builtins; with settings.lib; with flake-utils.lib; settings.mkOutputs {
        inherit inputs;
        callPackage = { stdenv, oreo, py, pname }: j.mkPythonPackage self stdenv [] (rec {
            owner = "syvlorg";
            inherit pname;
            src = ./.;
            propagatedBuildInputs = [ oreo py ];
            postPatch = ''
                substituteInPlace pyproject.toml --replace "oreo = { git = \"https://github.com/${owner}/oreo.git\", branch = \"main\" }" ""
                substituteInPlace setup.py --replace "'oreo @ git+https://github.com/${owner}/oreo.git@main'" ""
            '';
        });
        pname = "bakery";
        type = "hy";
    };
}
