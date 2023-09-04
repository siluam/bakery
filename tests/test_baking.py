from bakery import ls, ls as la, ls as ld, find
from oreo import is_nots
from os import sep
from pytest import mark


@mark.baking
class TestBaking:
    def test_baking(self, assorted_cookies, cookies):
        try:
            ls.bake_(cookies, a=True, _filter=is_nots, _list=True, _sort=None)
            assert ls() == assorted_cookies
        finally:
            ls.splat_()
            assert "a" not in ls._kwargs.baked[ls._subcommand.default]
            assert cookies not in ls._args.baked[ls._subcommand.default]

    def test_baking_program(self, assorted_cookies, cookies):
        try:
            ld.bake_(_sort=True)
            ls.bake_(cookies, programs_=True, _list=True)
            for item in la:
                assert item in assorted_cookies
            assert assorted_cookies[::-1] == ld()
        finally:
            ld.splat_(all_classes_=True)
            assert "_sort" not in ls._kwargs.baked[ls._subcommand.default]
            assert cookies not in ls._args.program[ls._program]

    def test_baking_all_programs(self, assorted_cookies, cookies):
        try:
            ls.bake_(cookies, world_=True, _filter=is_nots, _list=True, _sort=None)
            assert (
                ls()
                == [item.removeprefix(str(cookies) + sep) for item in find()][1:]
                == assorted_cookies
            )
        finally:
            ls.splat_(world_=True)
            assert "_sort" not in ls._kwargs.baked[ls._subcommand.default]
            assert cookies not in ls._args.program[ls._program]
            assert "_sort" not in find._kwargs.baked[find._subcommand.default]
            assert cookies not in find._args.program[find._program]
