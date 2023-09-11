"""Custom Exception Module for ``JM Builder``

This module contains all custom exception for ``JM Builder`` package.

Copyright (c) 2023 Ryuu Mitsuki.


Available Classes
-----------------
JMException :
    The base custom exception for ``JM Builder`` package.

JMUnknownTypeError :
    The custom exception that raised when an unknown type error
    occurs during the execution of the package.

JMParserError :
    Raised when an error has occurred during parsing the configuration.

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

from .._globals import AUTHOR

__all__    = ['JMException', 'JMUnknownTypeError', 'JMParserError']
__author__ = AUTHOR


class JMException(Exception):
    """
    Base custom exception for ``JM Builder`` package.

    Parameters
    ----------
    *args :
        Variable length argument list.

    **kwargs :
        Arbitrary keyword arguments.

    Properties
    ----------
    __message : str or None
        The message of this exception.

        To specify the message of this exception, consider place the message
        string at first argument.

    __traces : traceback.StackSummary or None
        The stack traces of this exception. If no traceback is provided during
        the exception creation, it will be set to ``None`` and will be overrided
        by ``traceback.extract_stack()``.

        To specify the stack traces of this exception, consider use keyword
        `tb`, `trace` or `traces`, with the value separated by `=`.
        For example::

          # Use the `tb` keyword
          >>> JMException('An error occured', tb=foo)
          JMException('An error occured', with_traceback: 'True')

          # Use the `trace` keyword
          >>> JMException('An error occured', trace=foo)
          JMException('An error occured', with_traceback: 'True')

          # Use the `traces` keyword
          >>> JMException('An error occured', traces=foo)
          JMException('An error occured', with_traceback: 'True')

    Notes
    -----
    This custom exception extends the base `Exception` class and allows
    you to create a custom exception with an optional message and traceback
    information.

    """

    __message:  Optional[str]
    __traces:   Optional[_tb.StackSummary]

    def __init__(self, *args, **kwargs) -> None:
        """Initialize self. For accurate signature, see ``help(type(self))``."""

        baseerr: str = f'Error occured during initializing {type(self)}'
        tb_key:  str = None

        if len(args) > 0 and (args[0] and not isinstance(args[0], str)):
            raise self.__class__(baseerr) from \
                TypeError(
                    f'Invalid type of `message`: "{type(args[0]).__name__}". ' + \
                    'Expected "str"'
                )

        self.__message = None
        self.__traces  = None

        if len(args) > 1:
            try:
                self.__message = args[0] % args[1:]
            except TypeError as type_err:
                raise self.__class__(baseerr) from type_err

        elif len(args) == 1:
            self.__message = args[0]


        if 'tb' in kwargs:
            tb_key = 'tb'
        elif ('trace', 'traces') in kwargs:
            tb_key = 'trace' if 'trace' in kwargs else 'traces'
        else:
            self.__traces = _tb.extract_stack()

        if tb_key:
            if not isinstance(kwargs[tb_key], _tb.StackSummary):
                raise self.__class__(baseerr) from \
                    TypeError(
                        f'Invalid type of `tb`: "{type(kwargs[tb_key]).__name__}". ' +
                        'Expected "traceback.StackSummary"'
                    )

            self.__traces = kwargs.get(tb_key)
            del kwargs[tb_key]  # delete after stack traces retrieved

        super().__init__(self.__message, **kwargs)


    def __repr__(self) -> str:
        """
        Return ``repr(self)``.

        Returns
        -------
        str :
            The string representation of this exception, including the class name
            and the message of this exception (if specified), and the
            `with_traceback` with a stringized boolean value.

        Notes
        -----
        The `with_traceback` will have ``True`` value if and only if the
        stack traces are defined either given from initialization class
        or defaults to `traceback.extract_stack()`, otherwise ``False``
        if there is no stack traces defined in this exception.

        """
        return f"{self.__class__.__name__}({self.__message!r}, " + \
               f"with_traceback: '{bool(self.__traces)}')"

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
        bool
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
        Get the detail message of this exception.

        Returns
        -------
        str or None
            The message of this exception. If not specified, returns ``None``.
        """
        return self.__message

    @property
    def traces(self) -> _tb.StackSummary:
        """
        Get the stack traces of this exception.

        Returns
        -------
        traceback.StackSummary
            The stack traces of this exception. If not specified, returns
            the stack traces from ``traceback.extract_stack()``.
        """
        if self.__traces and isinstance(self.__traces, _tb.StackSummary):
            return self.__traces

        return _tb.extract_stack()



class JMUnknownTypeError(JMException, TypeError):
    """
    Custom exception for unknown type errors in the ``JM Builder`` package.

    This exception is raised when an unknown type error occurs during
    the execution of the package.

    Parameters
    ----------
    *args :
        Variable length argument list.

    **kwargs :
        Additional keyword arguments to customize the exception.

    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize self. See ``help(type(self))`` for accurate signature."""

        super().__init__(*args, **kwargs)
        self.__message = super().message
        self.__traces = super().traces

    @property
    def message(self) -> Optional[str]:
        """
        Get the detail message of this exception.

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
            the stack traces from `traceback.extract_stack()`.
        """
        if self.__traces and isinstance(self.__traces, _tb.StackSummary):
            return self.__traces

        return _tb.extract_stack()



class JMParserError(JMException):
    """
    Raised when an error has occurred during parsing the configuration.

    Parameters
    ----------
    *args :
        Variable length argument list.

    **kwargs :
        Additional keyword arguments to customize the exception.

    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize self. See ``help(type(self))`` for accurate signature."""

        super().__init__(*args, **kwargs)
        self.__message = super().message
        self.__traces = super().traces

    @property
    def message(self) -> Optional[str]:
        """
        Get the detail message of this exception.

        Returns
        -------
        str or None :
            The detail message of this exception. If not specified, returns ``None``.

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
            the stack traces from `traceback.extract_stack()`.

        """
        return self.__traces



# Remove unnecessary variables
del AUTHOR, Any, Optional, Union
