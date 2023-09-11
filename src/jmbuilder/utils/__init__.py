"""Utilities Module for JMBuilder

This module provide utilities for ``JMBuilder`` package.

Copyright (c) 2023 Ryuu Mitsuki.
"""

from . import logger, config
from .logger import *
from .config import *

from .._globals import AUTHOR

__author__ = AUTHOR

__all__ = ['logger', 'config']
__all__.extend(logger.__all__)
__all__.extend(config.__all__)

# Remove unnecessary variables
del AUTHOR
