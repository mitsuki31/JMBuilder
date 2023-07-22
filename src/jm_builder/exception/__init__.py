import sys
from _io import TextIOWrapper

STDOUT: TextIOWrapper = sys.stdout
STDERR: TextIOWrapper = sys.stderr

del sys, TextIOWrapper

try:
    from .exception import JMException
except ImportError:
    from exception import JMException
