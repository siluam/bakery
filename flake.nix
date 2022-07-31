{
    description = "An \"sh\" alternative!";
    inputs = rec {
        settings.url = github:sylvorg/settings;
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
        callPackage = { buildPythonPackage, pythonOlder, poetry-core, oreo, pytest-hy, pytest-randomly, pytestCheckHook, py, pname }: let
            owner = "syvlorg";
        in buildPythonPackage rec {
            inherit pname;
            version = j.pyVersion format src;
            format = "pyproject";
            disabled = pythonOlder "3.9";
            src = ./.;
            buildInputs = [ poetry-core ];
            nativeBuildInputs = buildInputs;
            propagatedBuildInputs = [ oreo py ];
            pythonImportsCheck = [ pname ];
            checkInputs = [ pytestCheckHook pytest-hy pytest-randomly ];
            checkPhase = "pytest --tb=native";
            postPatch = ''
                substituteInPlace pyproject.toml --replace "oreo = { git = \"https://github.com/${owner}/oreo.git\", branch = \"main\" }" ""
                substituteInPlace setup.py --replace "'oreo @ git+https://github.com/${owner}/oreo.git@main'" ""
            '';
            meta.homepage = "https://github.com/${owner}/${pname}";
        };
        pname = "bakery";
        type = "hy";
    };
}
