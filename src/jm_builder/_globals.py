"""Global Module for JMBuilder

All global variables and properties are defined in this module.

Copyright (c) 2023 Ryuu Mitsuki.

Available Classes
-----------------
_JMCustomPath
    This class provides all path variables that used by ``JMBuilder`` package.
    All path variables in this class are read-only properties.

Available Constants
-------------------
AUTHOR : str
    The author name.

BASEDIR : str
    Provides path to the base directory of this package.

CONFDIR : str
    Provides path to the specified directory that contains configuration
    files for configuring ``JMBuilder`` package, the path itself is
    relative to `BASEDIR`.

LOGSDIR : str
    Provides path to the temporary directory that used by this package,
    the path itself is relative to `BASEDIR`.

TMPDIR : str
    Provides path to the logs directory that used by this package,
    the path itself is relative to `BASEDIR`.
"""

import os as _os
import sys as _sys
from pathlib import Path as _Path
from typing import (
    Self as _Self,
    ClassVar as _ClassVar,
    Type as _Type,
    TypeVar as _TypeVar
)
from _io import TextIOWrapper as _TextIOWrapper

from .exception.jm_exc import JMUnknownTypeError as _JMTypeError

if '_global_imported' in globals():
    raise RuntimeError(
        "Cannot import the '_globals' more than once.")
_global_imported: bool = True

C = _TypeVar('C', bound=type)

class _JMCustomPath:
    """
    Custom class to manage read-only path variables for ``JMBuilder`` package.

    This class provides read-only properties for common path variables
    such as `basedir`, `tmpdir`, `logsdir` and more.

    Parameters
    ----------
    _type : type, optional
        The class type used for casting the path variables.
        Please note, this is experimental option, leave it empty to
        avoid unexpected issue.

        This argument are optional and can be assigned by any class.
        For example, cast the returned path into `Path` object.

        >>> from pathlib import Path
        >>> from jm_builder import _JMCustomPath

        # Create new object
        >>> path = _JMCustomPath(Path)
        >>> path.tmpdir
        PosixPath('.../tmp')  # for Windows, it will be `WindowsPath`

        # You can also check the class type that currently used for casting
        >>> path.type
        <class 'pathlib.Path'>

    Raises
    ------
    JMUnknownTypeError :
        If `_type` is not a class type.

    Attributes
    ----------
    __basedir : C
        The base directory path of this package.

    __confdir : C
        The path to specified directory that contains configuration
        files for configuring ``JMBuilder`` package, and the path is
        relative to `basedir`.

    __tmpdir : C
        The path to the 'tmp' directory relative to `basedir`.

    __logsdir : C
        The path to the 'logs' directory relative to `basedir`.

    __type : C
        Returns the current class type for casting the path.

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

    def __init__(self, _type: _Type[C] = str) -> _Self:
        """Initialize self. See ``help(type(self))``, for accurate signature."""
        self.__type = _type

        if not isinstance(_type, type):
            raise _JMTypeError(
                f'Unexpected type of `_type`: "{type(_type).__name__}". ' + \
                'Expected type is "type"')

        # Cast all attributes with the specified class type
        self.__basedir = self.__type(self.__basedir)
        self.__tmpdir  = self.__type(self.__tmpdir)
        self.__logsdir = self.__type(self.__logsdir)
        self.__confdir = self.__type(self.__confdir)

    @property
    def basedir(self) -> C:
        """
        The current working directory path based on parent directory of this file.

        Returns
        -------
        C -> type :
            The current working directory path.
        """
        return self.__basedir

    @property
    def tmpdir(self) -> C:
        """
        The path to 'tmp' directory relative to `basedir`.

        Returns
        -------
        C -> type :
            The path to temporary directory.
        """
        return self.__tmpdir

    @property
    def logsdir(self) -> C:
        """
        The path to 'logs' directory relative to `basedir`.

        Returns
        -------
        C -> type :
            The path to logs directory.
        """
        return self.__logsdir


    @property
    def confdir(self) -> C:
        """
        The path to '.config' directory relative to `basedir`.

        Returns
        -------
        C -> type :
            The path to the specified directory that contains configuration
            files for configuring ``JMBuilder`` package.
        """
        return self.__confdir

    @property
    def type(self) -> C:
        """
        Returns the current class type for casting the path.

        Returns
        -------
        Type[C] -> Type[type] :
            The current class type.
        """
        return self.__type


BASEDIR: str = _JMCustomPath().basedir
TMPDIR:  str = _JMCustomPath().tmpdir
LOGSDIR: str = _JMCustomPath().logsdir
CONFDIR: str = _JMCustomPath().confdir

STDOUT: _TextIOWrapper = _sys.stdout
STDERR: _TextIOWrapper = _sys.stderr


AUTHOR:  str = 'Ryuu Mitsuki'

__author__ = AUTHOR
__all__    = ['_JMCustomPath', 'BASEDIR', 'CONFDIR', 'LOGSDIR', 'TMPDIR', 'STDOUT', 'STDERR']

# Remove unnecessary variables
del AUTHOR, _os, _sys, _Self, _Path, _ClassVar, _Type, _TypeVar, C, _TextIOWrapper
