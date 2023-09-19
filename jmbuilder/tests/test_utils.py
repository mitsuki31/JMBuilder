"""
Test suite for utilities members and properties parser, exclusively
for `jmbuilder.utils` submodule.

Copyright (c) 2023 Ryuu Mitsuki

"""

import os
import json
import unittest

from .._globals import AUTHOR, CONFDIR
from .. import utils as jmutils

__author__ = AUTHOR
del AUTHOR


class TestUtilities(unittest.TestCase):
    """Test class for utilities functions."""

    # The path reference to JSON config file
    jsonfile: str = os.path.join(CONFDIR, 'setup.json')

    def test_jsonparser(self) -> None:
        """Test the `jmbuilder.utils.config.jsonparser` method."""
        # Check the existence of config file
        self.assertTrue(os.path.exists(self.jsonfile))

        # Get the config data
        jsondata: dict = jmutils.config.json_parser(self.jsonfile)
        self.assertIsNotNone(jsondata)
        self.assertIsInstance(jsondata, dict)

        jsondata_manual: dict = {}
        # Extract the JSON data manually and compare with the other one
        with open(self.jsonfile, 'r', encoding='utf-8') as file:
            jsondata_manual = json.load(file)

        self.assertDictEqual(jsondata, jsondata_manual)

    def test_setupinit(self) -> None:
        """Test the `jmbuilder.utils.config.setupinit` method."""
        jm_setup = jmutils.config.setupinit()
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


if __name__ == '__main__':
    unittest.main()
