"""Global Module for JMBuilder

All global variables and properties are defined in this module.

Copyright (c) 2023 Ryuu Mitsuki.

Available Classes
-----------------
_JMCustomPath
    This class provides all path variables that is used by ``JMBuilder`` package.
    All path variables in this class are read-only properties.

Available Constants
-------------------
AUTHOR : str
    The author name.

BASEDIR : str
    Provides path to the base directory of this package.

    This is alias for `_JMCustomPath().basedir`.

CONFDIR : str
    Provides path to the specified directory that contains configuration
    files for configuring ``JMBuilder`` package, the path itself is
    relative to `BASEDIR`.

    This is alias for `_JMCustomPath().confdir`.

LOGSDIR : str
    Provides path to the temporary directory that used by this package,
    the path itself is relative to `BASEDIR`.

    This is alias for `_JMCustomPath().logsdir`.

STDOUT : _io.TextIOWrapper
    This is alias for `sys.stdout` and referenced to console standard
    output.

STDERR : _io.TextIOWrapper
    This is alias for `sys.stderr` and referenced to console standard
    error.

TMPDIR : str
    Provides path to the logs directory that used by this package,
    the path itself is relative to `BASEDIR`.

    This is alias for `_JMCustomPath().tmpdir`.
"""

import os as _os
import sys as _sys
from pathlib import Path as _Path
from typing import (
    Type,
    TypeVar
)

from _io import TextIOWrapper as _TextIOWrapper


if '_global_imported' in globals():
    raise RuntimeError(
        "Cannot import the '_globals' module more than once.")
_global_imported: bool = True

C = TypeVar('C', bound=type)

class _JMCustomPath:
    """
    Custom class to manage read-only path variables for ``JMBuilder`` package.

    This class provides read-only properties for common path variables
    such as `basedir`, `tmpdir`, `logsdir` and more.

    Parameters
    ----------
    _type : type, optional
        The class type used for casting the path variables.
        Please note, this is experimental option, leave this empty to
        avoid unexpected issue.

        This argument are optional and can be assigned by any class.
        For example, cast the returned path into `Path` object::

          >>> from pathlib import Path
          >>> from jm_builder import _JMCustomPath

          # Create new object
          >>> path = _JMCustomPath(Path)
          >>> path.tmpdir
          PosixPath('.../tmp')  # if Windows, it will be `WindowsPath`

          # You can also check the class type that currently
          # used for casting
          >>> path.type
          <class 'pathlib.Path'>

    Raises
    ------
    TypeError :
        If `_type` is not a class `type`.

    Notes
    -----
    The path variables are read-only properties, and attempts to modify
    them will raise an ``AttributeError``.
    """

    __type:     C
    __basedir:  str = str(_Path(__file__).resolve().parent)
    __tmpdir:   str = _os.path.join(__basedir, 'tmp')
    __logsdir:  str = _os.path.join(__basedir, 'logs')
    __confdir:  str = _os.path.join(__basedir, '.config')

    def __init__(self, _type: Type[C] = str) -> None:
        """Initialize self. See ``help(type(self))``, for accurate signature."""
        self.__type = _type

        if not isinstance(_type, type):
            raise TypeError(
                f'Invalid type of `_type`: "{type(_type).__name__}". ' + \
                'Expected "type"')

        # Cast all attributes with the specified class type
        self.__basedir = self.__type(self.__basedir)
        self.__tmpdir  = self.__type(self.__tmpdir)
        self.__logsdir = self.__type(self.__logsdir)
        self.__confdir = self.__type(self.__confdir)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(type: {self.__type.__name__!r})'

    @property
    def basedir(self) -> C:
        """
        The current working directory path based on parent directory of this file.

        Returns
        -------
        C :
            The current working directory path.
        """
        return self.__basedir

    @property
    def tmpdir(self) -> C:
        """
        The path to 'tmp' directory relative to `basedir`.

        Returns
        -------
        C :
            The path to temporary directory.
        """
        return self.__tmpdir

    @property
    def logsdir(self) -> C:
        """
        The path to 'logs' directory relative to `basedir`.

        Returns
        -------
        C :
            The path to logs directory.
        """
        return self.__logsdir

    @property
    def confdir(self) -> C:
        """
        The path to '.config' directory relative to `basedir`.

        Returns
        -------
        C :
            The path to the specified directory that contains configuration
            files for configuring ``JMBuilder`` package.
        """
        return self.__confdir

    @property
    def type(self) -> Type[C]:
        """
        Returns the current class type for casting the path.

        Returns
        -------
        Type[C] :
            The class type.
        """
        return self.__type


# Aliases
BASEDIR: str = _JMCustomPath().basedir
TMPDIR:  str = _JMCustomPath().tmpdir
LOGSDIR: str = _JMCustomPath().logsdir
CONFDIR: str = _JMCustomPath().confdir

STDOUT: _TextIOWrapper = _sys.stdout
STDERR: _TextIOWrapper = _sys.stderr


AUTHOR:  str = 'Ryuu Mitsuki'

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
    del _os, _sys, _Path, _TextIOWrapper

# ...except for these variables, can be safely removed
del C, Type, TypeVar
