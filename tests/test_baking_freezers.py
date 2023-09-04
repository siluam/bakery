from bakery import ls, tail
from oreo import first_last_n, is_nots
from parametrized import parametrized
from pytest import fixture, mark
from typing import Callable


@mark.baking
@mark.piping
class TestBakeryFreezer:
    @fixture
    def tails(self, cookies, scope="class"):
        return ls([], cookies, a=True) | tail

    @parametrized
    def test_bake_freezer(
        self,
        assorted_cookies,
        tails,
        fhash=(
            lambda tails: tails._freezer_hash,
            lambda tails: hash(tuple(tails._freezer)),
        ),
    ):
        fhash = fhash(tails) if isinstance(fhash, Callable) else fhash
        try:
            ls.bake_(freezer_hash_=fhash, _list=True, _sort=None, _filter=is_nots)
            assert (
                first_last_n(assorted_cookies, last=True, number=10, type_=list)
                == tails()
            )
            assert not isinstance(ls(), list)
        finally:
            ls.splat_(freezer_hash_=fhash)
            assert "_sort" not in tails._kwargs.freezer[fhash]

    def test_bake_freezer_no_args_non_attr_kwargs(
        self, assorted_cookies, cookies, tails
    ):
        try:
            tails.bake_(cookies, help=True, _list=True, _sort=None, _filter=is_nots)
            assert (
                first_last_n(assorted_cookies, last=True, number=10, type_=list)
                == tails()
            )
        finally:
            tails.splat_()
            assert "_sort" not in tails._kwargs.baked[tails._subcommand.default]

    @parametrized.zip
    def test_piping_macro_baking(
        self,
        assorted_cookies,
        cookies,
        tails,
        opts=(
            {"base_programs_": True},
            {"base_program_": "ls"},
            {"programs_": True},
            {"program_": "ls"},
            {"freezers_": True},
            lambda tails: {"freezer_hash_": tails._freezer_hash},
            lambda tails: {"freezer_hash_": hash(tuple(tails._freezer))},
        ),
        cls=(
            "base_program",
            "base_program",
            "program",
            "program",
            "freezer",
            "freezer",
            "freezer",
        ),
    ):
        opts = opts if isinstance(opts, dict) else opts(tails)
        try:
            tails.bake_(
                cookies, help=True, _list=True, _sort=None, _filter=is_nots, **opts
            )
            assert (
                first_last_n(assorted_cookies, last=True, number=10, type_=list)
                == tails()
            )
        finally:
            tails.splat_(**opts)
            k = next(iter(opts.keys()))
            v = next(iter(opts.values()))
            assert (
                "_sort"
                not in tails._kwargs[cls][
                    tails._freezer_hash
                    if k == "freezers_"
                    else getattr(tails, "_" + cls)
                    if isinstance(v, bool)
                    else v
                ]
            )

    @parametrized.zip
    def test_bake_freezer_failures(
        self,
        assorted_cookies,
        cookies,
        tails,
        opts=({"base_program_": "tail"}, {"program_": "tail"}),
        cls=("base_program", "program"),
    ):
        try:
            tails.bake_(
                cookies, help=True, _list=True, _sort=None, _filter=is_nots, **opts
            )
            assert (
                not first_last_n(assorted_cookies, last=True, number=10, type_=list)
                == tails()
            )
        finally:
            tails.splat_(**opts)
            assert "_sort" not in tails._kwargs[cls][next(iter(opts.values()))]
