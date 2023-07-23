"""Global Module for ``JM Builder``

All global variables and properties are defined in this module.

Copyright (c) 2023 Ryuu Mitsuki.
"""

import os as _os
from pathlib import Path as _Path
from typing import (
    Self as _Self,
    ClassVar as _ClassVar,
    Type as _Type,
    TypeVar as _TypeVar
)

if '_global_imported' in globals():
    raise RuntimeError(
        "Cannot import the '_globals' more than once.")
_global_imported: bool = True

C = _TypeVar('C', bound=type)

class _JMCustomPath:
    """
    Custom class to manage read-only path variables for ``JM Builder`` package.

    This class provides read-only properties for common path variables
    such as `basedir`, `tmpdir` and `logsdir`.

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
    TypeError :
        If `_type` is not a class type.

    Attributes
    ----------
    basedir : C
        The base directory path of this package.

    tmpdir : C
        The path to the 'tmp' directory relative to `basedir`.

    logsdir : C
        The path to the 'logs' directory relative to `basedir`.

    type : C
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

    def __init__(self, _type: _Type[C] = str) -> _Self:
        """Initialize self. See ``help(type(self))``, for accurate signature."""
        self.__type = _type

        if not isinstance(_type, type):
            raise TypeError(
                f'Unexpected type of `_type`: "{type(_type).__name__}". ' + \
                'Expected type is a class type')

        self.__basedir = self.__type(self.__basedir)
        self.__tmpdir  = self.__type(self.__tmpdir)
        self.__logsdir = self.__type(self.__logsdir)

    @property
    def basedir(self) -> C:
        """The current working directory path."""
        return self.__basedir

    @property
    def tmpdir(self) -> C:
        """The path to 'tmp' directory relative to `basedir`."""
        return self.__tmpdir

    @property
    def logsdir(self) -> C:
        """The path to 'logs' directory relative to `basedir`."""
        return self.__logsdir

    @property
    def type(self) -> C:
        """Returns the current class type for casting the path."""
        return self.__type


BASEDIR: str = _JMCustomPath().basedir
TMPDIR:  str = _JMCustomPath().tmpdir
LOGSDIR: str = _JMCustomPath().logsdir

AUTHOR:  str = 'Ryuu Mitsuki'

__author__ = AUTHOR
__all__    = ['BASEDIR', 'LOGSDIR', 'TMPDIR', '_JMCustomPath']

# Remove unnecessary variables
del _os, _Self, _Path, _ClassVar, _Type, _TypeVar, C
