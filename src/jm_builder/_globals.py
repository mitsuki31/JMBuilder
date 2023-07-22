import os as _os

if '_global_imported' in globals():
    raise RuntimeError(
        "Cannot import the '_globals' more than once.")
_global_imported: bool = True

BASEDIR: str = _os.getcwd()
TMPDIR:  str = _os.path.join(BASEDIR, 'tmp')
LOGSDIR: str = _os.path.join(BASEDIR, 'logs')

AUTHOR:  str = 'Ryuu Mitsuki'

__author__ = AUTHOR
__all__    = ['AUTHOR', 'BASEDIR', 'LOGSDIR', 'TMPDIR']

# Remove unnecessary variables
del _os
