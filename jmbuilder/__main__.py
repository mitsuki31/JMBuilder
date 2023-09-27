"""Main Module for JMBuilder

Copyright (c) 2023 Ryuu Mitsuki.

"""

import os as __os
import sys as __sys
from pathlib import Path as __Path
from typing import Any, Union, TextIO


try:
    from ._globals import AUTHOR, VERSION, VERSION_INFO, __jmsetup__
except (ImportError, ModuleNotFoundError, ValueError):
    # Add a new Python search path to the first index
    __sys.path.insert(0, str(__Path(__sys.path[0]).parent))

    from jmbuilder._globals import AUTHOR, VERSION, VERSION_INFO, __jmsetup__
finally:
    del __Path  # This no longer being used


def __print_version(exit: bool = False, *,
                    only_ver: bool = False,
                    file: TextIO = __sys.stdout) -> None:
    """
    Print the version info to specific opened file.

    Parameters
    ----------
    exit : bool, optional
        Whether to exit and terminate the Python after printed the version.
        Defaults to False (disabled).

    only_ver: bool, optional
        Whether to print the version only. By activating this option,
        other information like program name, license, and copyright
        will not be printed. Defaults to False.

    file : TextIO, optional
        The file to print the version info.
        Defaults to console standard output (`sys.stdout`).

    """

    if not file:
        raise ValueError("File must be an opened file object, not None")

    program_name: str = __jmsetup__.progname
    version:      str = f"v{'.'.join(map(str, __jmsetup__.version))}"
    author:       str = __jmsetup__.author

    # Check if only_ver is False (or not specified)
    if not only_ver:
        print(
            program_name, version, f'- {__jmsetup__.license}',  # Program name and version
            __os.linesep + \
            f'Copyright (C) 2023 by {author}.',                 # Copyright notice
            file=file
        )
    else:
        print(version, file=file)

    if exit:
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
    only_version_args: tuple = ('-VV', '--only-ver', '--only-version')

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

    # To print the version only, user can use several arguments. See 'only_version_args'
    elif __argchck(only_version_args, args):
        __print_version(True, only_ver=True)


    # ... Still in development


__author__       = AUTHOR
__version__      = VERSION
__version_info__ = VERSION_INFO


# Delete unused imported objects
del AUTHOR, VERSION, VERSION_INFO
del Any, Union, TextIO


if __name__ == '__main__':
    main()
