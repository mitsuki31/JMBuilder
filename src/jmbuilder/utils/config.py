"""Config Parser Module for JMBuilder

This module provides some basic properties to parse configuration
files for ``JMBuilder`` package.

Copyright (c) 2023 Ryuu Mitsuki.


Available Functions
-------------------
_get_confdir
    This method returns the path to the configuration directory with
    the specified class type for casting the path. Defaults to `str`.

    The class type is only supported the `str` and `pathlib.Path`.
    For example::

      # Import the module
      >>> import pathlib
      >>> from jm_builder import _config

      # Get the path without argument, it will default returns `str`
      >>> _config._get_confdir()
      '/path/to/configuration/directory'

      # Get the path with argument and cast the path with `Path` class
      >>> _config._get_confdir(pathlib.Path)
      PosixPath('/path/to/configuration/directory')

    This method is alias for `_JMCustomPath(T).confdir`, with ``T``
    is the class type for cast the path.

json_parser
    This function provides an easy way to parses and retrieves all
    configurations from JSON configuration files.

    For example::

        >>> json_parser('path/to/configs_file.json')
        {'foo': False, 'bar': True}

"""

import os as _os
import sys as _sys
import json as _json
from pathlib import Path as _Path
from typing import (
    Optional,
    Union,
    Type
)

from .._globals import AUTHOR, CONFDIR
from ..exception.jm_exc import (
    JMUnknownTypeError as _JMTypeError,
    JMParserError as _JMParserError
)


__author__ = AUTHOR
__all__    = ['json_parser']
del AUTHOR


def _get_confdir(_type: Union[Type[str], Type[_Path]] = str) -> Union[str, _Path]:
    """
    Get the path to the configuration directory.

    Parameters
    ----------
    _type : type, optional
        The class type to cast the path. Defaults to Python's built-in
        string type (`str`).

    Returns
    -------
    str or pathlib.Path :
        The path to the configuration directory. The returned type is
        depends to class type that specified by `_type`.

    Raises
    ------
    JMUnknownTypeError :
        If the `_type` is not of class type `str` or `pathlib.Path`.

    Notes
    -----
    This function returns the path to the configuration directory,
    and you can specify the desired type of the output using the
    `_type` parameter. By default, it returns the path as a string.

    Example
    -------
    >>> jmbuilder._config.get_confdir()
    '/path/to/configuration/directory'

    >>> import pathlib
    >>> jmbuilder._config.get_confdir(pathlib.Path)
    PosixPath('/path/to/configuration/directory')
    """
    err = _JMTypeError(
        f'Unknown type: "{type(_type).__name__}". ' +
        'Expected "str" and "pathlib.Path"')

    if not (isinstance(_type, type) or isinstance(_type(), (str, _Path))):
        raise err

    return _type(CONFDIR)


def json_parser(path: Optional[str] = None) -> dict:
    """
    Parse and retrieve all configurations from specified JSON
    configuration file.

    Parameters
    ----------
    path : str or None, optional
        The path to specify the configuration file to be parsed.
        Defaults to `_get_confdir(str)`.

    Returns
    -------
    dict :
        A dictionary containing all parsed configurations from specified
        configuration file.

    Notes
    -----
    This function only supported configuration file with JSON type.
    Given file paths will be validated before retrieving their configurations,
    and check the extension file. Make sure the given path references
    to file with the `.json` extension.

    """
    if not path:
        raise ValueError(
            f"Unexpected value: '{type(path).__name__}'. Expected 'str'"
        ) from _JMParserError(
            "Something went wrong while parsing the configuration file"
        )

    # Raise an error if the given path not `str` type
    if not isinstance(path, str):
        raise _JMTypeError(
            f"Unknown type '{type(path).__name__}'. Expected 'str'"
        ) from _JMParserError(
            "Something went wrong while parsing the configuration file"
        )

    # Check existence
    if not _os.path.exists(path):
        raise FileNotFoundError(
            f"No such file or directory: '{path}'"
        ) from _JMParserError(
            'Configuration file was not found'
        )

    # Check whether a directory or regular file
    if _os.path.isdir(path):
        raise IsADirectoryError(
            f"Is a directory: '{path}'"
        ) from _JMParserError(
            'Directory found. No such configuration file'
        )

    # Check the extension file
    if not path.endswith('.json'):
        raise _JMParserError(
            'Unknown file type. No such JSON configuration file'
        )

    configs: dict = {}

    with open(path, 'r', encoding='utf-8') as cfg_file:
        contents: str = cfg_file.read()

        # Check for null to prevent an error on JSONDecoder
        if contents:
            configs = _json.loads(contents)  # return a dictionary

    return configs



class _JMSetupConfRetriever:
    """
    A class that retrieves and provides all setup configuration.

    Notes
    -----
    This class only retrieves the setup configuration without any modification
    methods to their values.

    """

    setupfile: str = _os.path.join(_get_confdir(str), 'setup.json')


    class FrozenJMVersion:
        """
        This class create frozen version for JMBuilder's version.

        Parameters
        ----------
        major : int
            The major version.

        minor : int
            The minor version.

        patch : int
            The patch version.

        """
        def __init__(self, major: int, minor: int, patch: int) -> None:
            """Initialize self."""
            self.__frozen_version: tuple = (major, minor, patch)

        def __repr__(self) -> str:
            """
            Return a string representation of the frozen version.

            Returns
            -------
            str :
                A string representation of the frozen version.

            """
            return f"{self.__class__.__name__}("         + \
                   f"major={self.__frozen_version[0]}, " + \
                   f"minor={self.__frozen_version[1]}, " + \
                   f"patch={self.__frozen_version[2]})"

        def __getitem__(self, index: int) -> int:
            """
            Get the version number with specified index.

            Parameters
            ----------
            index : int
                An index, the index must be 0 <= index < 3.

            Returns
            -------
            int :
                An integer representation the specified version number.

            """
            if 0 <= index < 3:
                return self.__frozen_version[index]

            raise IndexError(f'Index out of range: {index}')

        @property
        def major(self) -> int:
            """
            Get the major version from frozen version.

            Returns
            -------
            int :
                An integer representation of major version.

            """
            return self.__frozen_version[0]

        @property
        def minor(self) -> int:
            """
            Get the minot version from frozen version.

            Returns
            -------
            int :
                An integer representation of minor version.

            """
            return self.__frozen_version[1]

        @property
        def patch(self) -> int:
            """
            Get the patch version from frozen version.

            Returns
            -------
            int :
                An integer representation of patch version.

            """
            return self.__frozen_version[2]


    def __init__(self) -> None:
        """Initialize self."""

        # Get all properties
        configs: dict = json_parser(self.setupfile)

        ver: tuple = configs.get('Version')

        self.__jm_program_name: str = configs.get('Program-Name')
        self.__jm_version: self.FrozenJMVersion = self.FrozenJMVersion(ver[0], ver[1], ver[2])
        self.__jm_author: str = configs.get('Author')
        self.__jm_license: str = configs.get('License')

    @property
    def progname(self) -> str:
        """
        Get the program name from setup configuration.

        Returns
        -------
        str :
            A string representation of program name.

        """
        return self.__jm_program_name

    @property
    def version(self) -> FrozenJMVersion:
        """
        Get the program version from setup configuration.

        Returns
        -------
        tuple :
            A tuple representation of program version.

        """
        return self.__jm_version

    @property
    def author(self) -> str:
        """
        Get the author name from setup configuration.

        Returns
        -------
        str :
            A string representation of author name.

        """
        return self.__jm_author

    @property
    def license(self) -> str:
        """
        Get the license name from setup configuration.

        Returns
        -------
        str :
            A string representation of license name.

        """
        return self.__jm_license


def setupinit() -> _JMSetupConfRetriever:
    """Do nothing. This is alias to `_JMSetupConfRetriever()`."""
    return _JMSetupConfRetriever()



# Delete unnecessary variables
del Optional, Union, Type
