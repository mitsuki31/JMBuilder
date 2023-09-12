"""Main Module for JMBuilder

Copyright (c) 2023 Ryuu Mitsuki.

"""

import os as __os
import sys as __sys
from pathlib import Path as __Path
from typing import Any, Union


try:
    from _globals import AUTHOR
    from utils import config as __config
except (ImportError, ModuleNotFoundError):
    # Add a new Python search path to the first index
    __sys.path.insert(0, str(__Path(__sys.path[0]).parent))
    del __Path  # This no longer used

    from jmbuilder._globals import AUTHOR
    from jmbuilder.utils import config as __config

__author__ = AUTHOR
del AUTHOR

def __print_version(_exit: bool = False) -> None:
    """
    Print the version info to standard output.

    Parameters
    ----------
    _exit : bool, optional
        Whether to exit and terminate the Python after printed the version.
        Defaults to False (disabled).

    """

    _setupcls: __config._JMSetupConfRetriever = __config.setupinit()

    program_name: str = _setupcls.progname
    version:      str = 'v' + '.'.join(str(v) for v in _setupcls.version)
    author:       str = _setupcls.author

    print(
        program_name, version,                                 # Program name and version
        __os.linesep + \
        f'Copyright (C) 2023 {author}. All rights reserved.',  # Copyright notice
        file=__sys.stdout
    )
    if _exit:
        __sys.exit(0)


def __argchck(targets: Any, args: Union[list, tuple]) -> bool:
    """
    Check whether specified argument are presented in `args`.

    Paramaters
    ----------
    targets : Any
        An argument or a list of arguments to searched for.

    args : list or tuple
        A list of arguments.

    Returns
    -------
    bool :
        Returns True if the specified argument are presented in `args`,
        otherwise returns False.

    """
    if isinstance(targets, str):
        return targets in args

    found: bool = False
    for target in targets:
        if target in args:
            found = True

    return found


#::#  Main Driver  #::#
def main() -> None:
    """Main function for JMBuilder."""
    version_args: tuple = ('-V', '--version',)

    # Trim the file name from command line arguments (at the first index)
    args: list = __sys.argv[1:]

    if __argchck(version_args, args):
        __print_version(_exit=True)


    # ... Still in development



# Delete unnecessary imported objects
del Any, Union


if __name__ == '__main__':
    main()
