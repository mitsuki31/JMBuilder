"""Config Parser Module for JMBuilder

This module provides some basic properties to parse configuration
files for ``JMBuilder`` package.

Copyright (c) 2023 Ryuu Mitsuki.


Available Functions
-------------------
_get_confdir
    This utility function returns the path to the configuration directory with
    the specified class type for casting the path. Defaults to `str`.

    The class type is only supported the `str` and `pathlib.Path`.

    Examples::

      # Get the path without argument, it will default returns `str`
      >>> _get_confdir()
      '/path/to/configuration/directory'

      # Get the path with argument and cast the path with `Path` class
      >>> _get_confdir(pathlib.Path)
      PosixPath('/path/to/configuration/directory')

    This function is alias for `jmbuilder._JMCustomPath(T).confdir`, with `T`
    is the class type for cast the path.

json_parser
    This utility function provides an easy way to parses and retrieves all
    configurations from JSON configuration files.

    Examples::

        >>> json_parser('path/to/configs_file.json')
        {'foo': False, 'bar': True}

setupinit
    This utility function is alias function to initialize the `_JMSetupConfRetriever`.

remove_comments
    This utility function can remove lines from a list of strings representing
    the file contents that starting with a specified delimiter and returns
    a new list with lines starting with a specified delimiter removed.
    This function are designed for removing comments lines from file contents.

    Examples::

        # Read file contents
        >>> contents = []
        >>> with open('path/to/example.txt') as f:
        ...     contents = f.readlines()
        ...
        >>> contents
        ['Hello', '# This is comment line', 'World']

        >>> remove_comments(contents, delim='#')
        ['Hello', 'World']

remove_blanks
    This utility function can remove blank lines from the list of strings
    representing the file contents, and optionally remove lines with value `None`.
    Return a new list with blank lines removed.

    Examples::

        >>> contents = ['', 'Foo', None, '', '1234']
        >>> remove_blanks(contents, none=False)  # Ignore None
        ['Foo', None, '1234']

        >>> remove_blanks(contents, none=True)
        ['Foo', '1234']

"""

import os as _os
import io as _io
import sys as _sys
import json as _json
import locale as _locale
import collections as _collections
from pathlib import Path as _Path
from typing import (
    List,
    Optional,
    Union,
    Type,
    TextIO
)

from .._globals import AUTHOR, CONFDIR
from ..exception.jm_exc import (
    JMUnknownTypeError as _JMTypeError,
    JMParserError as _JMParserError
)


__author__ = AUTHOR
__all__    = ['json_parser', 'remove_comments', 'remove_blanks']
del AUTHOR


def _get_confdir(_type: Union[Type[str], Type[_Path]] = str) -> Union[str, _Path]:
    """
    Get the path to the configuration directory.

    Parameters
    ----------
    _type : type, optional
        The class type to cast the path. Defaults to Python's built-in
        string type (`str`). Supported type is `str` and `pathlib.Path`.

    Returns
    -------
    str or pathlib.Path :
        The path to the configuration directory. The returned type is
        depends to class type that specified by `_type`.

    Raises
    ------
    JMUnknownTypeError :
        If the `_type` is not of class type `str` or `pathlib.Path`.

    Notes
    -----
    This function returns the path to the configuration directory,
    and users can specify the desired type of the output using the
    `_type` parameter. By default, it returns the path as a string.

    Examples
    --------
    >>> jmbuilder._config.get_confdir()
    '/path/to/configuration/directory'

    >>> import pathlib
    >>> jmbuilder._config.get_confdir(pathlib.Path)
    PosixPath('/path/to/configuration/directory')
    """
    err = _JMTypeError(
        f'Unknown type: "{type(_type).__name__}". ' +
        'Expected "str" and "pathlib.Path"')

    if not (isinstance(_type, type) or isinstance(_type(), (str, _Path))):
        raise err

    return _type(CONFDIR)


def json_parser(path: str) -> dict:
    """
    Parse and retrieve all configurations from specified JSON
    configuration file.

    Parameters
    ----------
    path : str
        The path to specify the configuration file to be parsed.

    Returns
    -------
    dict :
        A dictionary containing all parsed configurations from specified
        configuration file.

    Raises
    ------
    JMParserError :
        If something went wrong during parsing the configuration file.

    ValueError :
        If the given path is `None`.

    JMUnknownTypeError :
        If the given path's type are not `str`.

    FileNotFoundError :
        If the given path are refers to a non-existing file.

    IsADirectoryError :
        If the given path are refers to a directory instead a configuration file.

    Notes
    -----
    This function only supported configuration file with JSON type.
    Given file paths will be validated before retrieving their configurations,
    and check the extension file. Make sure the given path references
    to file with the `.json` extension.

    """
    if not path:
        raise ValueError(
            f"Unexpected value: '{type(path).__name__}'. Expected 'str'"
        ) from _JMParserError(
            "Something went wrong while parsing the configuration file"
        )

    # Raise an error if the given path not `str` type
    if not isinstance(path, str):
        raise _JMTypeError(
            f"Unknown type '{type(path).__name__}'. Expected 'str'"
        ) from _JMParserError(
            "Something went wrong while parsing the configuration file"
        )

    # Check existence
    if not _os.path.exists(path):
        raise FileNotFoundError(
            f"No such file or directory: '{path}'"
        ) from _JMParserError(
            'Configuration file was not found'
        )

    # Check whether a directory or regular file
    if _os.path.isdir(path):
        raise IsADirectoryError(
            f"Is a directory: '{path}'"
        ) from _JMParserError(
            'Directory found. No such configuration file'
        )

    # Check the extension file
    if not path.endswith('.json'):
        raise _JMParserError(
            'Unknown file type. No such JSON configuration file'
        )

    configs: dict = {}

    with open(path, 'r', encoding='utf-8') as cfg_file:
        contents: str = cfg_file.read()

        # Check for null to prevent an error on JSONDecoder
        if contents:
            configs = _json.loads(contents)  # return a dictionary

    return configs



def remove_comments(contents: List[str], delim: str = '#') -> List[str]:
    """
    Remove lines starting with a specified delimiter.

    This function removes lines from the input list of contents that start
    with the specified delimiter. It returns a new contents with comments removed.

    Parameters
    ----------
    contents : List[str]
        A list of strings representing the contents of a file.

    delim : str, optional
        The delimiter used to identify comment lines. Lines starting with
        this delimiter will be removed. The default is '#'.

    Returns
    -------
    List[str] :
        A new contents with comment lines (specified by delimiter) removed.

    Raises
    ------
    ValueError :
        If the input list `contents` is empty.

    Notes
    -----
    Multiple specified delimiters cannot be removed in a single call to
    this function. Although the problem can be fixed by executing the
    procedure as many times depending on the delimiters that need
    to be removed. But still it is not a convenient way.

    Examples::

        # Suppose we want to remove lines that starting with
        # hashtags (#) and exclamation marks (!).
        >>> remove_comments(
        ...     remove_comments(contents, delim='#'), delim='!')

    """
    if not contents or len(contents) == 0:
        raise ValueError('File contents cannot be empty')

    # Use a list comprehension to filter out lines starting with the delimiter
    return [line for line in contents if not line.startswith(delim)]



def remove_blanks(contents: List[str], none: bool = True) -> List[str]:
    """
    Remove empty lines from a list of strings.

    This function removes empty lines (lines with no content) and lines
    containing only whitespace from the input list of strings. Optionally,
    it can removes lines containing `None`.

    Parameters
    ----------
    contents : List[str]
        A list of strings representing the contents of a file.

    none : bool, optional
        If True, lines containing `None` are also removed.
        If False, only lines with no content are removed. The default is True.

    Returns
    -------
    List[str] :
        A new contents with empty lines removed.

    Raises
    ------
    ValueError :
        If the input list `contents` is empty.

    """
    if not contents or len(contents) == 0:
        raise ValueError('File contents cannot be empty')

    if none:
        return [line for line in contents if line or line.strip() != '']

    return [line for line in contents if line.strip() != '']



class _JMSetupConfRetriever:
    """
    A class that retrieves and provides all setup configuration.

    Attributes
    ----------
    setupfile :
        A string path reference to the setup configuration file.

    Notes
    -----
    This class only retrieves the setup configuration without any modification
    methods to their values.

    """

    setupfile: str = _os.path.join(_get_confdir(str), 'setup.json')


    class FrozenJMVersion:
        """
        This class create frozen version for JMBuilder's version.

        Parameters
        ----------
        major : int
            The major version.

        minor : int
            The minor version.

        patch : int
            The patch version.

        """
        def __init__(self, major: int, minor: int, patch: int) -> None:
            """Initialize self."""
            self.__frozen_version: tuple = (major, minor, patch)

        def __repr__(self) -> str:
            """
            Return a string representation of the frozen version.

            Returns
            -------
            str :
                A string representation of the frozen version.

            """
            return f"{self.__class__.__name__}("         + \
                   f"major={self.__frozen_version[0]}, " + \
                   f"minor={self.__frozen_version[1]}, " + \
                   f"patch={self.__frozen_version[2]})"

        def __getitem__(self, index: int) -> int:
            """
            Get the version number with specified index.

            Parameters
            ----------
            index : int
                An index, the index must be 0 <= index < 3.

            Returns
            -------
            int :
                An integer representation the specified version number.

            Raises
            ------
            IndexError :
                If the given index is negative or greater than 2.

            """
            if 0 <= index < 3:
                return self.__frozen_version[index]

            raise IndexError(f'Index out of range: {index}')

        @property
        def major(self) -> int:
            """
            Get the major version from frozen version.

            Returns
            -------
            int :
                An integer representation of major version.

            """
            return self.__frozen_version[0]

        @property
        def minor(self) -> int:
            """
            Get the minot version from frozen version.

            Returns
            -------
            int :
                An integer representation of minor version.

            """
            return self.__frozen_version[1]

        @property
        def patch(self) -> int:
            """
            Get the patch version from frozen version.

            Returns
            -------
            int :
                An integer representation of patch version.

            """
            return self.__frozen_version[2]


    def __init__(self) -> None:
        """Initialize self."""

        # Get all properties
        configs: dict = json_parser(self.setupfile)

        ver: tuple = configs.get('Version')

        self.__jm_program_name: str = configs.get('Program-Name')
        self.__jm_version: self.FrozenJMVersion = self.FrozenJMVersion(ver[0], ver[1], ver[2])
        self.__jm_author: str = configs.get('Author')
        self.__jm_license: str = configs.get('License')

    @property
    def progname(self) -> str:
        """
        Get the program name from setup configuration.

        Returns
        -------
        str :
            A string representing the program name.

        """
        return self.__jm_program_name

    @property
    def version(self) -> FrozenJMVersion:
        """
        Get the program version from setup configuration.

        Returns
        -------
        tuple :
            A tuple representing the module version.

        """
        return self.__jm_version

    @property
    def author(self) -> str:
        """
        Get the author name from setup configuration.

        Returns
        -------
        str :
            A string representing the author name.

        """
        return self.__jm_author

    @property
    def license(self) -> str:
        """
        Get the license name from setup configuration.

        Returns
        -------
        str :
            A string representing the license name.

        """
        return self.__jm_license


def setupinit() -> _JMSetupConfRetriever:
    """Do nothing. This is alias to `_JMSetupConfRetriever()`."""
    return _JMSetupConfRetriever()



class JMProperties(_collections.UserDict):
    """
    This class provides a convenient way to parse properties files
    and access their contents.

    Parameters
    ----------
    filename : str or TextIO
        The filename or file object to read properties from. If a filename is
        provided, it checks for the file's existence, opens the file stream,
        and retrieves the properties. If a file object is provided, it directly
        reads the properties from it.

    encoding : str, optional
        The encoding to use when opening the file stream. If not specified,
        it uses the encoding from `locale.getpreferredencoding()`.

    Attributes
    ----------
    data : dict
        A dictionary containing all the parsed properties.

    filename : str
        The path to the property file.

    Raises
    ------
    JMParserError :
        If an error occurs while reading and parsing the properties file.

    FileNotFoundError :
        If the specified file path does not exist.

    ValueError :
        If the `filename` parameter is None.

    """
    def __init__(self, filename: Union[str, TextIO], *,
                 encoding: str = None) -> None:
        """Initialize self."""

        if isinstance(filename, str):
            self.filename = _os.path.abspath(filename)

        # If encoding is not specified, use the system's preferred encoding
        encoding = encoding if encoding else _locale.getencoding()

        # Raise FileNotFoundError, if the given file are not exist
        # First these code below will checks whether the given file is not None
        # and its type is `str`
        if self.filename and \
                isinstance(self.filename, str) and \
                not _os.path.exists(self.filename):
            raise FileNotFoundError(f"File not found: '{filename}'") \
                from _JMParserError(
                    'The specified path does not reference any property file ' +
                    'or the file does not exist'
                )
        elif not self.filename:
            raise ValueError('The file parameter cannot be None')

        self.data = {}
        contents: list = []

        # Open and read the contents if the given file is of type `str`
        if isinstance(filename, str):
            with open(filename, 'r', encoding=encoding) as prop:
                contents = prop.readlines()
        elif isinstance(filename, _io.TextIOWrapper):
            contents = filename.readlines()

            # Get the name of property file
            self.filename = filename.name

        # Define lambda functions to clean and split lines
        blank_remover = lambda line: line.strip()
        colon_splitter = lambda line: line.split(':', maxsplit=1)
        equalsign_splitter = lambda line: line.split('=', maxsplit=1)

        # Extract file contents, remove comments and empty strings
        contents = list(map(blank_remover, contents))
        contents = remove_comments(contents, '#')
        contents = remove_blanks(contents, none=True)

        # First, try to split the keys and values using equals sign (=) as a delimiter
        data: Optional[list] = list(map(equalsign_splitter, contents))
        keys, values = None, None

        # Check if the first try has extracted the keys and values successfully
        # If the length of each element is one, it indicates extraction failure,
        # so we try splitting using a colon (:) as a delimiter
        if data and len(data[0]) == 1:
            # In this second try, use a colon (:) as a delimiter
            # for keys and values
            data = list(map(colon_splitter, contents))

        try:
            # Unpack keys and values into variables (errors can occur here)
            keys, values = zip(*data)
        except (ValueError, TypeError) as type_val_err:
            raise type_val_err from _JMParserError(
                'Unable to unpack keys and values'
            )

        # Remove trailing whitespace in keys and values
        keys = tuple(map(blank_remover, keys))
        values = tuple(map(blank_remover, values))

        # Build the dictionary from extracted keys and values
        self.data = dict(zip(keys, values))



# Delete unnecessary variables
del List, Optional, Union, Type, TextIO
