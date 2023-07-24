"""JMBuilder package

JMBuilder or JMatrixBuilder, provides some utilities to build the ``JMatrix``.
For more information about ``JMatrix``, you can refer to link below.

    https://github.com/mitsuki31/jmatrix.git

Available Classes
-----------------
JMException
    This class is a base exception for this package.

_JMCustomPath
    This class provides all path variables that used by ``JMBuilder`` package.
    All path variables in this class are read-only properties.

Available Constants
-------------------
BASEDIR
    Provides a string that represents the path to base directory
    of this package.

LOGSDIR
    Provides a string that represents the path to logs directory
    that being used by this package to log some information and errors.

STDOUT
    References the console standard output (`sys.stdout`).

STDERR
    References the console standard error (`sys.stderr`).

TMPDIR
    Provides a string that represents the path to temporary directory
    that being used by this package to store some temporary file(s) or cache(s).
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
