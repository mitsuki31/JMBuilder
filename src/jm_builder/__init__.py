"""JMBuilder package

JMBuilder or JMatrixBuilder, provides some utilities to build the ``JMatrix``.
For more information about ``JMatrix``, you can refer to link below.

    https://github.com/mitsuki31/jmatrix.git

Available Classes
-----------------
JMException
    This class is a base exception for this package.

_JMCustomPath
    This class provides all path variables that used by ``JM Builder`` package.
    All path variables in this class are read-only properties.

Available Constants
-------------------

"""

from . import exception
from .exception import *
from . import utils
from .utils import *
from . import _globals
from ._globals import AUTHOR
from ._globals import *

__author__ = AUTHOR

__all__ = []
__all__.extend(_globals.__all__)
__all__.extend(exception.__all__)
__all__.extend(utils.__all__)

# Remove unnecessary variables
del AUTHOR
