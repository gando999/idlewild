import os
import pytest

from idlewild.schematools import parse_and_build_idl_file

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def test_stuff():
    schema = parse_and_build_idl_file(
        os.path.join(__location__, 'starwars.graphqls')
    )
    assert schema is not None

