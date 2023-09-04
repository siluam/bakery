from os import environ
from pytest import mark
from valiant import SuperPath

if not (no_git := environ.get("NIX_ENFORCE_PURITY", 0)):
    try:
        from bakery import git
    except ImportError:
        no_git = True


@mark.git_remote
@mark.skipif(condition=no_git, reason="Git may not be available on some systems.")
def test_git_status(request):
    assert git(C=SuperPath(request.config.rootdir)).remote(_str=True) == "origin"
