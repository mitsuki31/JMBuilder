"""Custom Exception Module for JMBuilder

This module contains all custom exception for ``JMBuilder`` package.

Copyright (c) 2023 Ryuu Mitsuki.

Available Classes
-----------------
JMException
    The base custom exception for ``JMBuilder`` package.

JMUnknownTypeError
    The custom exception that raised when an unknown type error
    occurs during the execution of the package.
"""

import os as _os
import sys as _sys
import traceback as _tb
from datetime import datetime as _dtime
from typing import (
    Optional,
    Union,
    Any
)

# Please note, that 'typing.Self' only supported on
# Python 3.11 and later. For earlier version, here we just simply
# create a global variable with name the same as 'Self'
if _sys.version_info < (3, 11):
    global Self
    Self = None
else:
    from typing import Self

from .._globals import AUTHOR

__all__    = ['JMException', 'JMUnknownTypeError']
__author__ = AUTHOR
del AUTHOR

class JMException(Exception):
    """
    Base custom exception for ``JMBuilder`` package.

    Parameters
    ----------
    *args
        Variable length argument list.

    **kwargs
        Arbitrary keyword arguments.

    Properties
    ----------
    message : str or None
        The message of this exception.

        To specify the message of this exception, consider place the message
        string at first argument.

    traces : traceback.StackSummary or None
        The stack traces of this exception. If no traceback is provided during
        the exception creation, it will be set to ``None`` and will be overrided
        by ``traceback.extract_stack()``.

        To specify the stack traces of this exception, consider use keyword
        `trace` or `traces`, with the value separated by `=`. For example::

        # Use the `trace` keyword
        >>> JMException('An error occured', trace=foo)

        # Use the `traces` keyword
        >>> JMException('An error occured', traces=foo)

    Notes
    -----
    This custom exception extends the base ``Exception`` class and allows you to create
    a custom exception with an optional message and traceback information.
    """

    __message:  Optional[str]
    __traces:   Optional[_tb.StackSummary]

    def __init__(self, *args, **kwargs) -> Self:
        """Initialize self. For accurate signature, see ``help(type(self))``."""

        if len(args) > 0 and (args[0] and not isinstance(args[0], str)):
            raise self.__class__(
                f'Error occured during initializing {type(self)}') from \
                TypeError(
                    f'Unexpected type of `message`: "{type(args[0]).__name__}". ' + \
                    'Expected type is "str"'
                )

        if len(args) > 1:
            self.__message = args[0] % args[1:]

        self.__message = args[0] if len(args) > 0 else None
        self.__traces  = None

        if 'tb' in kwargs:
            self._traces = kwargs.get('tb') or _tb.extract_stack()
            del kwargs['tb']
        elif ('trace', 'traces') in kwargs:
            self._traces = kwargs.get('trace', kwargs.get('traces')) or _tb.extract_stack()
            try:
                del kwargs['trace']
            except KeyError:
                del kwargs['traces']
        else:
            self._traces = _tb.extract_stack()

        super().__init__(self.__message, **kwargs)

    def __repr__(self) -> str:
        """
        Return ``repr(self)``.

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
        Return the string representation of this exception's message.

        Returns
        -------
        str :
            The message of this exception.

        Notes
        -----
        This method will never returns ``NoneType`` when the message are not specified,
        instead it returns the empty string.
        """
        return f'{self.__message}' if self.__message is not None else ''

    def __eq__(self, other: Any) -> bool:
        """
        Return ``self==value``.

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
        if isinstance(other, (self.__class__, str)):
            return str(self) == str(other)

        return False


    @property
    def message(self) -> Optional[str]:
        """
        Get the message of this exception.

        Returns
        -------
        str or None:
            The message of this exception. If not specified, returns ``None``.
        """
        return self.__message

    @property
    def traces(self) -> _tb.StackSummary:
        """
        Get the stack traces of this exception.

        Returns
        -------
        traceback.StackSummary :
            The stack traces of this exception. If not specified, returns
            the stack traces from ``traceback.extract_stack()``.
        """
        if self.__traces and isinstance(self.__traces, _tb.StackSummary):
            return self.__traces

        return _tb.extract_stack()



class JMUnknownTypeError(JMException, TypeError):
    """
    Custom exception for unknown type errors in the ``JMBuilder`` package.

    This exception is raised when an unknown type error occurs during
    the execution of the package.

    Parameters
    ----------
    msg : str, optional
        The error message to be displayed. If not specified, the message
        will be set to ``None``.

    **kwargs
        Additional keyword arguments to customize the exception.

    Attributes
    ----------
    message : str or None
        The message of this exception.

    traces : traceback.StackSummary or None
        The stack traces of this exception. If no traceback is provided during
        the exception creation, it will be set to ``None`` and will be overrided
        by ``traceback.extract_stack()``.
    """

    __message: Optional[str]
    __traces:  Optional[_tb.StackSummary]

    def __init__(self, *args, **kwargs) -> Self:
        """Initialize self. See ``help(type(self))`` for accurate signature."""

        super().__init__(*args, **kwargs)
        self.__message = super().message
        self.__traces = super().traces

    @property
    def message(self) -> Optional[str]:
        """
        Get the message of this exception.

        Returns
        -------
        str or None :
            The message of this exception. If not specified, returns ``None``.
        """
        return self.__message

    @property
    def traces(self) -> _tb.StackSummary:
        """
        Get the stack traces of this exception.

        Returns
        -------
        traceback.StackSummary :
            The stack traces of this exception. If not specified, returns
            the stack traces from ``traceback.extract_stack()``.
        """
        if self.__traces and isinstance(self.__traces, _tb.StackSummary):
            return self.__traces

        return _tb.extract_stack()


# Remove unnecessary variables
del Any, Optional, Union, Self
