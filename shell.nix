with builtins; with (import (fetchGit {
    url = "https://github.com/shadowrylander/shadowrylander";
    ref = "main";
})).legacyPackages.${currentSystem}; mkShell {
    buildInputs = with python310Packages; [ poetry2setup (bakery.overridePythonAttrs (prev: { src = ./.; })) ];
}
