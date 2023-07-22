"""Custom Logger Module

This module provides a custom logger utility that initializes and creates a new
`Logger` object for logging information or errors to the console or a log file.

To use the custom logger in your project, you can import the `init_logger` function
from this module and create a new `Logger` object with desired settings.

Example:
    # Import the module
    >>> import logger

    # Create a new logger object
    >>> log = logger.init_logger(fmt=logger.CUSTOM_FORMAT,
    ...                          level=logger.INFO)
    >>> log
    <RootLogger root (DEBUG)>

    # Log some information message
    # The output would be printed to console standard error (stderr),
    # because the `filename` are not defined on `init_logger`.
    >>> log.info('This is an information message.')
    This is an information message.

    >>> try:
    ...     x = 3 / 0
    ... except ZeroDivisionError as div_err:
    ...     log.error('An error occurred.',
    ...               exc_info=div_err)
    An error occurred.
    Traceback (most recent call last):
    ...
    ZeroDivisionError: division by zero
"""

import os as _os
import sys as _sys
import logging as _log
from typing import Union as _Union

from .._globals import AUTHOR
from ..exception import STDERR
from ..exception.jm_exc import JMException as _JME


__all__ = [
    'init_logger', 'BASIC_FORMAT', 'CUSTOM_FORMAT',
    'NOTSET', 'DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL', 'FATAL'
]
__author__ = AUTHOR


# References of formatter
BASIC_FORMAT  = _log.BASIC_FORMAT
CUSTOM_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# References of logging levels
NOTSET   = _log.NOTSET      # 0
DEBUG    = _log.DEBUG       # 10
INFO     = _log.INFO        # 20
WARN     = _log.WARN        # 30
WARNING  = _log.WARNING     # 30
ERROR    = _log.ERROR       # 40
CRITICAL = _log.CRITICAL    # 50
FATAL    = _log.FATAL       # 50


def init_logger(filename: str = None, *, fmt: _Union[str, _log.Formatter] = None,
                level: int = DEBUG) -> _log.Logger:
    """
    Initializes and creates a new `Logger` object.

    Parameters
    ----------
    filename : {str, None}, optional
        A string representing the name of the logger file. If specified,
        logs will be written to the specified file, otherwise logs
        will be printed to `stderr` (standard error). Default is ``None``.

    fmt : {str, logging.Formatter}, optional
        A string representation of the log formatter or an object
        of `logging.Formatter` class. If not specified, a customized
        formatter will be used. Default is ``None``.

    level : int, optional
        An integer value that specifies the logging level for the logger.
        Default is ``logger.DEBUG`` (equal to 10).

    Returns
    -------
    logging.Logger :
        A new `Logger` object for logging any information or errors.

    Raises
    ------
    TypeError :
        If the 'fmt' are not instance of `str` or `logging.Formatter` class.
    """

    handler: _log.Handler

    # Check whether the 'filename' is defined
    if filename is None:
        handler = _log.StreamHandler(STDERR)
    elif filename:
        if not filename.endswith('.log'):
            filename += '.log'

        # Check whether the parent directory of 'filename' exist
        if not _os.path.exists(_os.path.dirname(filename)):
            # Create the directory if not exist
            _os.mkdir(_os.path.dirname(filename))
        handler = _log.FileHandler(filename)

    # Check whether the 'fmt' as log formatter is defined
    if fmt is None:
        handler.setFormatter(_log.Formatter(CUSTOM_FORMAT))
    elif fmt and isinstance(fmt, (str, _log.Formatter)):
        if isinstance(fmt, str):
            handler.setFormatter(_log.Formatter(fmt))
        else:
            handler.setFormatter(fmt)
    else:
        raise TypeError(
            'Expected are `str` and `logging.Formatter`') from \
        _JME('Invalid type argument')

    logger = _log.getLogger(_os.path.basename(filename)) if filename else _log.getLogger()
    logger.setLevel(level)      # set the logger level, default is DEBUG
    logger.addHandler(handler)  # set the handler

    return logger
