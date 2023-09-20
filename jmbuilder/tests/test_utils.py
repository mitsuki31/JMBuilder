"""
Test suite for utilities members and properties parser, exclusively
for `jmbuilder.utils` submodule.

Copyright (c) 2023 Ryuu Mitsuki

"""

import os
import json
import unittest
import pathlib

from .._globals import AUTHOR, CONFDIR
from .. import utils as jmutils

__author__ = AUTHOR
del AUTHOR


class TestUtilities(unittest.TestCase):
    """Test class for utilities functions."""

    # The path reference to JSON config file
    jsonfile: str = os.path.join(CONFDIR, 'setup.json')

    def test_get_confdir(self) -> None:
        """Test the `jmbuilder.utils.config._get_confdir` function."""
        test_obj = jmutils.config._get_confdir

        expected_types: tuple = (type(CONFDIR), pathlib.Path)
        expected_reprs: tuple = (repr(CONFDIR), repr(pathlib.Path(CONFDIR)))

        confdirs: tuple = (
            test_obj(expected_types[0]),
            test_obj(expected_types[1])
        )

        for i in range(2):
            self.assertIsInstance(confdirs[i], expected_types[i])
            self.assertEqual(repr(confdirs[0]), expected_reprs[0])

    def test_json_parser(self) -> None:
        """Test the `jmbuilder.utils.config.json_parser` function."""
        test_obj = jmutils.config.json_parser

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
        test_obj = jmutils.config.setupinit

        jm_setup = test_obj()
        jsondata: dict = jmutils.config.json_parser(self.jsonfile)

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
        test_obj = jmutils.config.remove_comments

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


if __name__ == '__main__':
    unittest.main()
