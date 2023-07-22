"""
"""

import os as _os
import sys as _sys
import traceback as _tb
from datetime import datetime as _dtime
from typing import (
    Optional as _Optional,
    Union as _Union,
    Any as _Any
)

from ..exception import STDOUT, STDERR
from .._globals import AUTHOR

__all__    = ['JMException']
__author__ = AUTHOR


class JMException(Exception):
    """
    Custom exception for ``jm_builder`` package.

    Parameters
    ----------
    msg : str, optional
        The message of this exception. If provided, it can contain format specifiers,
        and they will be filled with the arguments given to this constructor.
        Default is None.

    *args
        Variable length argument list.

    **kwargs
        Arbitrary keyword arguments.

    Attributes
    ----------
    message : str or None
        The formatted message of this exception. If no message is provided,
        it will be set to None.

    trace : traceback.StackSummary or None
        The stack traces of this exception. If no traceback is provided during
        the exception creation, it will be set to None.

    Notes
    -----
    This custom exception extends the base ``Exception`` class and allows you to create
    a custom exception with an optional message and traceback information.
    """

    __message: _Optional[str]
    __trace:   _Optional[_tb.StackSummary]

    def __init__(self, msg: str=None, *args, **kwargs) -> None:
        """Initialize self. For accurate signature, see ``help(type(self))``."""
        super().__init__(msg % args)
        self.__message = msg % args

        if not kwargs.get('tb') is None:
            self.__trace = kwargs.get('trace')
        else:
            self.__trace = _tb.extract_stack()

    def __repr__(self) -> str:
        """
        Returns ``repr(self)``.

        Returns
        -------
        str:
            The string representation of this exception, including the class name
            and the message of this exception.
        """
        return f"{self.__class__.__name__}('{self.__message}')"

    def __str__(self) -> str:
        """
        Returns the string representation of this exception's message.

        Returns
        -------
        str:
            The message of this exception.
        """
        return f"{self.__message}"

    def __eq__(self, other: _Any) -> bool:
        """
        Returns ``self==value``.

        Parameters
        ----------
        other : Any
            The object to compare with this exception.

        Returns
        -------
        bool:
            ``True`` if the given object are the same exception with the same message
            or if the given object are string with the same message as this exception,
            otherwise ``False``.
        """
        if isinstance(other, (self, str)):
            return str(self) == str(other)

        return False


    def get_message(self) -> _Optional[str]:
        """
        Returns the message of this exception.

        Returns
        -------
        str:
            The message of this exception. If not specified, returns ``None``.
        """
        return self.__message
