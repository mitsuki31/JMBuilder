"""Utilities Module for JMBuilder

This module provide utilities for ``JMBuilder`` package.

Copyright (c) 2023 Ryuu Mitsuki.
"""

from . import logger
from .logger import *

from .._globals import AUTHOR

__author__ = AUTHOR

__all__ = ['logger']
__all__.extend(logger.__all__)

# Remove unnecessary variables
del AUTHOR
