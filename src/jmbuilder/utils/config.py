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
    else:
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


# Delete unnecessary variables
del Optional, Union, Type
