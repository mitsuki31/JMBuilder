"""
Test suite for utilities members and properties parser, exclusively
for `jmbuilder.utils` submodule.

Copyright (c) 2023 Ryuu Mitsuki

"""

import os
import json
import unittest
import pathlib

from .. import setupinit
from .._globals import AUTHOR, CONFDIR
from ..utils import utils as jmutils

__author__ = AUTHOR
del AUTHOR


class TestUtilities(unittest.TestCase):
    """Test class for utilities functions."""

    # The path reference to JSON config file
    jsonfile: str = os.path.join(CONFDIR, 'setup.json')

    def test_json_parser(self) -> None:
        """Test the `jmbuilder.utils.config.json_parser` function."""
        test_obj = jmutils.json_parser

        # Check the existence of config file
        self.assertTrue(os.path.exists(self.jsonfile))

        # Get the config data
        jsondata: dict = test_obj(self.jsonfile)
        self.assertIsNotNone(jsondata)
        self.assertIsInstance(jsondata, dict)

        jsondata_manual: dict = {}
        # Extract the JSON data manually and compare with the other one
        with open(self.jsonfile, 'r', encoding='utf-8') as file:
            jsondata_manual = json.load(file)

        self.assertDictEqual(jsondata, jsondata_manual)

    def test_setupinit(self) -> None:
        """Test the `jmbuilder.utils.config.setupinit` function."""
        test_obj = setupinit

        jm_setup = test_obj()
        jsondata: dict = jmutils.json_parser(self.jsonfile)

        self.assertIsNotNone(jm_setup)  # First check that returned instance is not None

        # Create new dictionary from _JMSetupConfRetriever instance
        values: list = [
            jm_setup.progname,
            [jm_setup.version[i] for i in range(3)],
            jm_setup.author,
            jm_setup.license
        ]

        # Use the same key names with `jsondata.keys()`
        jm_setup = dict(zip(jsondata.keys(), values))

        # Check the equality for both dictionaries
        self.assertDictEqual(jm_setup, jsondata)


    def test_remove_comments(self) -> None:
        """Test the `jmbuilder.utils.config.remove_comments` function."""
        test_obj = jmutils.remove_comments

        contents: list = [
            'Hello, world!',
            '# This is a comment, you know.',
            '! This is also a comment',
            'Foo And Bar'
        ]

        expected_contents: tuple = (
            [
                'Hello, world!',
                '! This is also a comment',
                'Foo And Bar'
            ],
            [
                'Hello, world!',
                '# This is a comment, you know.',
                'Foo And Bar'
            ],
            [
                'Hello, world!',
                'Foo And Bar'
            ]
        )

        expected_delimiters: tuple = ('#', '!')

        for i, delimiter in enumerate(expected_delimiters):
            self.assertListEqual(
                test_obj(contents, delim=delimiter),
                expected_contents[i]
            )

        self.assertListEqual(test_obj(
            test_obj(contents, delim=expected_delimiters[0]),
            delim=expected_delimiters[1]
        ), expected_contents[2])

    def test_remove_blanks(self) -> None:
        """Test the `jmbuilder.utils.config.remove_blanks` function."""
        test_obj = jmutils.remove_blanks

        contents: list = [
            '',      # blank line
            'Not blank line',
            '    ',  # line with trailing whitespace
            None
        ]

        expected_contents: tuple = (
            [
                'Not blank line',
                None
            ],
            [
                'Not blank line'
            ]
        )


        len_exp_contents: int = len(expected_contents)
        for i in range(len_exp_contents):
            self.assertListEqual(
                # Pass any numbers other than zero to `bool` will returning True value,
                # including negative numbers
                test_obj(contents, none=bool(i)), expected_contents[i]
            )


if __name__ == '__main__':
    unittest.main()
