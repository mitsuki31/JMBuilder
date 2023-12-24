"""JMBuilder's core module.

Copyright (c) 2023 Ryuu Mitsuki.
"""

import os as _os
import sys as _sys
import re as _re
import bs4 as _bs4
from typing import Dict, List, Optional

from . import utils as _jmutils
from . import exception as _jmexc

try:
    from ._globals import AUTHOR, VERSION, VERSION_INFO
except (ImportError, ModuleNotFoundError, ValueError):
    from pathlib import Path

    # Add a new Python search path to the first index
    _sys.path.insert(0, str(Path(_sys.path[0]).parent))
    del Path

    from jmbuilder._globals import AUTHOR, VERSION, VERSION_INFO

class PomParser:
    """
    A class that provides an easy way to parse and get some useful
    informations from the provided POM file.

    Parameters
    ----------
    soup : BeautifulSoup
        A ``BeautifulSoup`` object.

    """
    
    def __init__(self, soup: _bs4.BeautifulSoup) -> '__Getter':
        """Create a new instance of ``__Getter`` class."""
        if not isinstance(soup, _bs4.BeautifulSoup):
            # Raise an error
            raise TypeError(f'Invalid instance class: {soup.__class__}')

        self.soup: _bs4.BeautifulSoup = soup
        self.project_tag: _bs4.element.Tag = soup.find('project')

    @staticmethod
    def parse(pom_file: str, encoding: str = 'UTF-8') -> 'PomParser':
        """
        Parse the POM file (``pom.xml``) and return the instance of
        this class. All comments and blank lines will be removed, keeping
        the contents of POM clean.

        Parameters
        ----------
        pom_file : str
            A string representing the path of pom.xml file to be parsed.

        encoding : str, optional
            The encoding to be used while parsing the pom.xml file.
            Defaults to UTF-8.

        Returns
        -------
        PomParser :
            An instance of this class.

        """

        # Read and convert the pom.xml file to BeautifulSoup object
        soup: _bs4.BeautifulSoup = _bs4.BeautifulSoup(
            ''.join(_jmutils.readfile(pom_file)), 'xml')

        # Find the comments using lambda, then extract them
        for element in soup(text=lambda t: isinstance(t, _bs4.Comment)):
            element.extract()

        # Return the instance of this class
        return PomParser(soup)

    def get_name(self) -> str:
        return self.project_tag.find('name').text  # => project.name

    def get_version(self) -> str:
        return self.project_tag.find('version').text  # => project.version

    def get_id(self) -> Dict[str, str]:
        return {  # Return a dictionary
            'groupId': self.project_tag.find('groupId').text,       # => project.groupId
            'artifactId': self.project_tag.find('artifactId').text  # => project.artifactId
        }

    def get_url(self) -> str:
        return self.project_tag.find('url').text  # => project.url

    def get_inception_year(self) -> str:
        return self.project_tag.find('inceptionYear').text  # => project.inceptionYear

    def get_author(self) -> Dict[str, str]:
        # => project.developers[0].developer
        author_element: _bs4.element.Tag = \
            self.project_tag.find('developers').find('developer')

        return {  # Return a dictionary
            'id': author_element.find('id').text,
            'name': author_element.find('name').text,
            'url': author_element.find('url').text
        }

    def get_license(self) -> Dict[str, str]:
        # => project.licenses[0].license
        license_element: _bs4.element.Tag = \
            self.project_tag.find('licenses').find('license')

        return {
            'name': license_element.find('name').text,
            'url': license_element.find('url').text,
            'distribution': license_element.find('distribution').text
        }

    def get_property(self, key: str, dot: bool = True) -> Optional[str]:
        # Raise an error if the provided key is an empty string or None
        if not (key or len(key)):
            raise ValueError('Key argument cannot be empty.')

        # Remove the 'properties' string tag
        key = key.replace('properties.', '') \
            if key.startswith('properties.') else key

        # Only split the dots if 'dot' argument enabled
        keys: List[str] = key.split('.') if dot else [key]
        # Add the prefix of 'properties' element tag
        if not dot or (dot and keys[0] != 'properties'):
            keys.insert(0, 'properties')  # Append to the first index

        result: _bs4.element.Tag = self.soup.find(keys[0])
        for k in keys[1:]:
            # Break if the result is empty or none
            if not result:
                break
            result = result.find(k)

        # The returned value could be a NoneType value
        return result.text if result else result


__author__       = AUTHOR
__version__      = VERSION
__version_info__ = VERSION_INFO

# Delete unused variables
del AUTHOR, VERSION, VERSION_INFO
