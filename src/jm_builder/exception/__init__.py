import sys as _sys
from _io import TextIOWrapper as _TextIOWrapper

STDOUT: _TextIOWrapper = _sys.stdout
STDERR: _TextIOWrapper = _sys.stderr

from . import jm_exc
from .jm_exc import *
from .._globals import AUTHOR

__author__ = AUTHOR

__all__ = ['jm_exc', 'STDERR', 'STDOUT']
__all__.extend(jm_exc.__all__)

# Remove unnecessary variables
del _sys, _TextIOWrapper, AUTHOR
