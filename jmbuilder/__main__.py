"""Main Module for JMBuilder

Copyright (c) 2023 Ryuu Mitsuki.

"""

import os as __os
import sys as __sys
from pathlib import Path as __Path
from typing import Any, Union, TextIO


try:
    from _globals import AUTHOR
    from utils import config as __config
except (ImportError, ModuleNotFoundError, ValueError):
    # Add a new Python search path to the first index
    __sys.path.insert(0, str(__Path(__sys.path[0]).parent))
    del __Path  # This no longer used

    from jmbuilder._globals import AUTHOR
    from jmbuilder.utils import config as __config

__author__ = AUTHOR
del AUTHOR

def __print_version(_exit: bool = False, *, file: TextIO = __sys.stdout) -> None:
    """
    Print the version info to specific opened file.

    Parameters
    ----------
    _exit : bool, optional
        Whether to exit and terminate the Python after printed the version.
        Defaults to False (disabled).

    file : TextIO, optional
        The file to print the version info.
        Defaults to console standard output (`sys.stdout`).

    """

    if not file:
        raise ValueError("File must be an opened file object, not None")

    _setupcls: __config._JMSetupConfRetriever = __config.setupinit()

    program_name: str = _setupcls.progname
    version:      str = f"v{'.'.join(map(str, _setupcls.version))}"
    author:       str = _setupcls.author

    print(
        program_name, version,                                 # Program name and version
        __os.linesep + \
        f'Copyright (C) 2023 {author}. All rights reserved.',  # Copyright notice
        file=file
    )
    if _exit:
        __sys.exit(0)


def __argchck(targets: Any, args: Union[list, tuple]) -> bool:
    """
    Check whether specified argument are presented in `args`.

    Paramaters
    ----------
    targets : Any
        An argument or a list of arguments (must iterable) to searched for.

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
        if str(target) in args:
            found = True

    return found


#::#  Main Driver  #::#
def main() -> None:
    """Main function for JMBuilder."""
    version_args: tuple = ('-V', '--version',)

    # Trim the file name from command line arguments (at the first index)
    args: list = __sys.argv[1:]

    # Check for `-V` or `--version` in the arguments
    # If found, print the version info then exit with exit code zero (success)
    #
    if __argchck(version_args, args):
        __print_version(True)

    # For `-version` argument, the output will be redirected
    # to the standard error (`sys.stderr`)
    #   `-V`, `--version` -> sys.stdout
    #   `-version`        -> sys.stderr
    #
    elif __argchck('-version', args):
        __print_version(True, file=__sys.stderr)


    # ... Still in development



# Delete unnecessary imported objects
del Any, Union, TextIO


if __name__ == '__main__':
    main()
