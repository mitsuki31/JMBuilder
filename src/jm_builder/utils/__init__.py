from . import logger
from .logger import *

from .._globals import AUTHOR

__author__ = AUTHOR
del AUTHOR

__all__ = ['logger']
__all__.extend(logger.__all__)
