"""Global Module for ``JM Builder``

This module contains all global variables, constants, and classes
used by the ``JM Builder`` package. It provides access to various
path variables and other configurations used throughout the package.

Copyright (c) 2023 Ryuu Mitsuki.


Available Classes
-----------------
_JMCustomPath :
    A custom class that provides all path variables used by
    the ``JM Builder`` package. All path variables in this class
    are read-only properties, this means they cannot be modified.


Available Constants
-------------------
AUTHOR : str
    The name of the author of the ``JM Builder`` package.

BASEDIR : str or pathlib.Path
    Provides the path to the base directory of the ``JM Builder`` package.

    This is an alias for `_JMCustomPath().basedir`.

CONFDIR : str or pathlib.Path
    Provides the path to the directory that contains configuration
    files for configuring the ``JM Builder`` package. The path itself
    is relative to `BASEDIR`.

    This is an alias for `_JMCustomPath().confdir`.

LOGSDIR : str or pathlib.Path
    Provides the path to the directory used for logging by the
    ``JM Builder`` package. The path itself is relative to `BASEDIR`.

    This is an alias for `_JMCustomPath().logsdir`.

STDOUT : TextIO
    An alias for `sys.stdout`, representing the standard output console.

STDERR : TextIO
    An alias for `sys.stderr`, representing the standard error console.

TMPDIR : str or pathlib.Path
    Provides the path to the temporary directory used by the
    ``JM Builder`` package. The path itself is relative to `BASEDIR`.

    This is an alias for `_JMCustomPath().tmpdir`.


Notes
-----
The `_JMCustomPath` class contains read-only properties for the path
variables, and attempts to modify them will raise an `AttributeError`.

"""

import os as _os
import sys as _sys
from pathlib import Path as _Path
from typing import (
    TextIO,
    Type,
    TypeVar,
    Union
)

if '_global_imported' in globals():
    raise RuntimeError(
        "Cannot import the '_globals' module more than once.")
_global_imported: bool = True

class _JMCustomPath:
    """
    Custom class to manage read-only path variables for ``JM Builder`` package.

    This class provides read-only properties for common path variables
    such as `basedir`, `tmpdir`, `logsdir` and more.

    Parameters
    ----------
    _type : type[str, pathlib.Path], optional
        The class type used for casting the path variables. Defaults to
        Python built-in string class (`str`).

        This parameter only supported the following types:
            - `str`
            - `pathlib.Path`

    Raises
    ------
    TypeError
        If `_type` is not a class of `str` neither `pathlib.Path`.

    Notes
    -----
    The path variables are read-only properties, and attempts to modify
    them will raise an ``AttributeError``.

    Examples
    --------
      >>> from pathlib import Path
      >>> from jm_builder import _JMCustomPath

      # Use `pathlib.Path` to cast the path
      >>> _JMCustomPath(Path).tmpdir
      PosixPath('.../tmp')  # if Windows, it will be `WindowsPath`

      # `str` type is the default value
      >>> _JMCustomPath().basedir
      '/path/to/base/directory/package'

      # You can also check the class type that currently
      # used for casting
      >>> _JMCustomPath(Path).type
      <class 'pathlib.Path'>

      # Attempt to modify the value will cause an error
      >>> _JMCustomPath().basedir = '/path/to/another/directory'
      Traceback (most recent call last):
        ...
      AttributeError: can't set attribute


    """

    __type:     type
    __basedir:  str = str(_Path(__file__).resolve().parent)
    __tmpdir:   str = _os.path.join(__basedir, 'tmp')
    __logsdir:  str = _os.path.join(__basedir, 'logs')
    __confdir:  str = _os.path.join(__basedir, '.config')

    def __init__(self, _type: type = str) -> None:
        """Initialize self. See ``help(type(self))``, for accurate signature."""
        self.__type = _type
        err = 'Invalid type of `_type`: "%s". ' + \
              'Expected "str" and "pathlib.Path"'

        if not isinstance(_type, type):
            err = TypeError(err % type(_type).__name__)
            raise err
        elif isinstance(_type, type) and \
                 _type.__name__ not in ('str', 'Path', 'pathlib.Path'):
            err = TypeError(err % _type.__name__)
            raise err

        # Cast all attributes with the specified class type
        self.__basedir = self.__type(self.__basedir)
        self.__tmpdir  = self.__type(self.__tmpdir)
        self.__logsdir = self.__type(self.__logsdir)
        self.__confdir = self.__type(self.__confdir)

    def __repr__(self) -> str:
        """
        Return the string represents the class name and the class type.

        Returns
        -------
        str
            A string representation of this class.
        """
        return f'{self.__class__.__name__}(type: {self.__type.__name__!r})'

    @property
    def basedir(self) -> Union[str, _Path]:
        """
        The current working directory path based on parent directory of this file.

        Returns
        -------
        str or pathlib.Path
            The current working directory path.
        """
        return self.__basedir

    @property
    def tmpdir(self) -> Union[str, _Path]:
        """
        The path to 'tmp' directory relative to `basedir`.

        Returns
        -------
        str or pathlib.Path
            The path to temporary directory.
        """
        return self.__tmpdir

    @property
    def logsdir(self) -> Union[str, _Path]:
        """
        The path to 'logs' directory relative to `basedir`.

        Returns
        -------
        str or pathlib.Path
            The path to logs directory.
        """
        return self.__logsdir

    @property
    def confdir(self) -> Union[str, _Path]:
        """
        The path to '.config' directory relative to `basedir`.

        Returns
        -------
        str or pathlib.Path
            The path to the specified directory that contains configuration
            files for configuring ``JMBuilder`` package.
        """
        return self.__confdir

    @property
    def type(self) -> Type[Union[str, _Path]]:
        """
        Return the current class type for casting the path.

        Returns
        -------
        Type[str] or Type[pathlib.Path]
            The class type.
        """
        return self.__type


# Aliases
BASEDIR: Union[str, _Path] = _JMCustomPath().basedir
TMPDIR:  Union[str, _Path] = _JMCustomPath().tmpdir
LOGSDIR: Union[str, _Path] = _JMCustomPath().logsdir
CONFDIR: Union[str, _Path] = _JMCustomPath().confdir

STDOUT: TextIO = _sys.stdout
STDERR: TextIO = _sys.stderr

AUTHOR: str    = 'Ryuu Mitsuki'

__author__ = AUTHOR
__all__    = [
    '_JMCustomPath',
    'BASEDIR', 'CONFDIR',
    'LOGSDIR', 'TMPDIR',
    'STDOUT', 'STDERR'
]

# Remove unnecessary variables,
# only if the Python version is 3.11 and later...
if _sys.version_info >= (3, 11):
    del _os, _sys, _Path

# ...except for these variables, they can be safely deleted
del Type, TypeVar, TextIO, Union
