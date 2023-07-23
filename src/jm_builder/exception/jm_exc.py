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
    Base custom exception for ``jm_builder`` package.

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

    traces : traceback.StackSummary or None
        The stack traces of this exception. If no traceback is provided during
        the exception creation, it will be set to None and will be overrided
        by ``traceback.extract_stack()``.

    Notes
    -----
    This custom exception extends the base ``Exception`` class and allows you to create
    a custom exception with an optional message and traceback information.
    """

    __message:  _Optional[str]
    __traces:   _Optional[_tb.StackSummary]

    def __init__(self, msg: str=None, *args, **kwargs) -> None:
        """Initialize self. For accurate signature, see ``help(type(self))``."""

        if msg and not isinstance(msg, str):
            raise TypeError(
                f'Unexpected type of `msg`: "{type(msg)}". Expected type are str')

        if msg:
            self.__message = msg % args
        else:
            self.__message = msg

        super().__init__(self.__message)

        if 'tb' in kwargs:
            self.__traces = kwargs.get('tb')
        elif ('trace', 'traces') in kwargs:
            self.__traces = kwargs.get('trace', 'traces')
        else:
            self.__traces = _tb.extract_stack()

    def __repr__(self) -> str:
        """
        Returns ``repr(self)``.

        Returns
        -------
        str :
            The string representation of this exception, including the class name
            and the message of this exception (if specified).
        """
        if self.__message is None:
            return f"{self.__class__.__name__}()"

        return f"{self.__class__.__name__}({self.__message!r})"

    def __str__(self) -> str:
        """
        Returns the string representation of this exception's message.

        Returns
        -------
        str :
            The message of this exception.

        Notes
        -----
        This method would not returns ``NoneType`` when the message are not specified,
        instead it returns the empty string.

        """
        return f'{self.__message}' if self.__message is not None else ''

    def __eq__(self, other: _Any) -> bool:
        """
        Returns ``self==value``.

        Parameters
        ----------
        other : Any
            The object to compare with this exception.

        Returns
        -------
        bool :
            ``True`` if the given object are the same exception with the same message
            or if the given object are string with the same message as this exception,
            otherwise ``False``.
        """
        if isinstance(other, (self, str)):
            return str(self) == str(other)

        return False


    @property
    def message(self) -> _Optional[str]:
        """
        Returns the message of this exception.

        Returns
        -------
        str or None:
            The message of this exception. If not specified, returns ``None``.
        """
        return self.__message

    @property
    def traces(self) -> _tb.StackSummary:
        """
        Returns the stack traces of this exception.

        Returns
        -------
        traceback.StackSummary :
            The stack traces of this exception. If not specified, returns
            the stack traces from ``traceback.extract_stack()``.
        """
        if self.__traces and isinstance(self.__traces, _tb.StackSummary):
            return self.__traces

        return _tb.extract_stack()
