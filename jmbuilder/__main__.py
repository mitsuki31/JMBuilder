"""Main Module for JMBuilder

Copyright (c) 2023 Ryuu Mitsuki.

"""

import os as __os
import sys as __sys
import re as __re
from pathlib import Path as __Path
from typing import Iterable, Union, List, Tuple, TextIO


try:
    from . import utils as __jmutils
    from ._globals import AUTHOR, VERSION, VERSION_INFO, __jmsetup__
except (ImportError, ModuleNotFoundError, ValueError):
    # Add a new Python search path to the first index
    __sys.path.insert(0, str(__Path(__sys.path[0]).parent))

    from . import utils as __jmutils
    from jmbuilder._globals import AUTHOR, VERSION, VERSION_INFO, __jmsetup__
finally:
    del __Path  # This no longer being used

CLEAN_ARGS: Tuple[str] = __jmutils.remove_duplicates(__sys.argv[1:])

def __print_version(_exit: bool = False, *,
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
        raise ValueError(f"File must be a file object, got {type(file).__name__!r}")

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

    if _exit:
        __sys.exit(0)


def __argchck(targets: Union[str, Iterable], args: Union[List[str], Tuple[str]]) -> bool:
    """
    Check whether specified argument are presented in `args`.

    Paramaters
    ----------
    targets : str or Iterable
        An argument or a list of arguments (must iterable) to searched for.

    args : list or tuple of str
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


def __find_arg(val: Union[str, __re.Pattern]) -> int:
    """
    Find the index of specified argument from the command-line arguments.

    Parameters
    ----------
    val : str or re.Pattern
        A regular expression pattern used to search for the argument within
        the command-line arguments. Accepts a string literal representing
        the regular expression or a compiled regular expression.

    Returns
    -------
    int :
        The index of the specified argument in the command-line arguments.
        Returns -1 if the argument cannot be found or if the command-line
        arguments are empty.

    Notes
    -----
    This function utilizes the global constant ``CLEAN_ARGS``, ensuring that
    it searches for the desired argument within the command-line arguments
    with all duplicate arguments omitted.

    """
    # Use the fixed arguments; global constant
    if len(CLEAN_ARGS) == 0:
        return -1

    # Convert to regular expression
    val = __re.compile(val) if isinstance(val, str) else val

    res: __re.Match = None
    for arg in CLEAN_ARGS:
        res = val.search(arg)
        if res:
            break

    return CLEAN_ARGS.index(res.group()) if res else -1


def __print_help() -> None:
    """Print the help message to the standard output."""

    program_name: str = __jmsetup__.progname
    version:      str = f"v{'.'.join(map(str, __jmsetup__.version))}"
    author:       str = __jmsetup__.author

    header: str = f'{program_name} {version}'

    print(f"""\
{header}
{''.join(['-' for _ in range(len(header))])}

USAGE:
   python -m jmbuilder [OPTIONS]

OPTIONS:
   -V, --version, -version
        Print the version and copyright. All of them will print
        directly to the standard output, except for '-version'.

   -VV, --only-ver, --only-version
        Print the version number only.

   -h, --help
        Print this help message.

ISSUES:
   Report some issues and help us improve this builder.
   <https://github.com/mitsuki31/JMBuilder/issues/new>

AUTHOR:
   {author}\
""")


#::#  Main Driver  #::#
def main() -> None:
    """Main function for JMBuilder."""
    help_args: Tuple[str] = ('-h', '--help')
    version_args: Tuple[str] = ('-V', '--version',)
    only_version_args: Tuple[str] = ('-VV', '--only-ver', '--only-version')

    # Trim the file name from command line arguments (at the first index)
    args: List[str] = __sys.argv[1:]

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

    # Print the help message
    elif __argchck(help_args, args):
        __print_help()

    # ... Still in development


__author__       = AUTHOR
__version__      = VERSION
__version_info__ = VERSION_INFO


# Delete unused imported objects
del AUTHOR, VERSION, VERSION_INFO
del Iterable, Union, TextIO, List, Tuple


if __name__ == '__main__':
    main()
