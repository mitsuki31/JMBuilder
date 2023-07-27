"""Exception Module for JMBuilder

This module contains several custom exception for ``JMBuilder`` package.

Copyright (c) 2023 Ryuu Mitsuki.


Available Classes
-----------------
JMException
    This is base exception class for all custom exception classes in
    this module and this class extends to `Exception` class.

JMUnknownTypeError
    This class extends to `JMException` and raised when an unknown type
    error occurs during the execution of the package.
"""

from . import jm_exc
from .jm_exc import *
from .._globals import AUTHOR

__author__ = AUTHOR

__all__ = ['jm_exc']
__all__.extend(jm_exc.__all__)

# Remove unnecessary variables
del AUTHOR
