"""Utilities Module for JMBuilder

This module provide utilities for `JMBuilder` package.

Copyright (c) 2023 Ryuu Mitsuki.
"""

from . import logger, utils
from .logger import *
from .utils import *

from .._globals import AUTHOR

__author__ = AUTHOR

__all__ = ['logger', 'utils']
__all__.extend(logger.__all__)
__all__.extend(utils.__all__)

# Remove unnecessary variables
del AUTHOR
