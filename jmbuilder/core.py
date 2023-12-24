"""JMBuilder's core module.

Copyright (c) 2023 Ryuu Mitsuki.
"""

import os as _os
import sys as _sys
import re as _re
import bs4 as _bs4
from typing import Dict, List, Optional, Union

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
    A class that provides an easy way to parse and retrieve useful
    information from the provided POM file.

    Parameters
    ----------
    soup : BeautifulSoup
        A `bs4.BeautifulSoup` object representing the parsed POM file.

    """
    
    def __init__(self, soup: _bs4.BeautifulSoup) -> 'PomParser':
        """Create a new instance of ``PomParser`` class."""
        if not isinstance(soup, _bs4.BeautifulSoup):
            # Raise an error
            raise TypeError(f'Invalid instance class: {soup.__class__}')

        self.soup: _bs4.BeautifulSoup = soup
        self.project_tag: _bs4.element.Tag = soup.find('project')

    @staticmethod
    def parse(pom_file: str, encoding: str = 'UTF-8') -> 'PomParser':
        """
        Parse the POM file (``pom.xml``) and return an instance of
        this class. Remove comments and blank lines to keep the POM clean.

        Parameters
        ----------
        pom_file : str
            The path of the pom.xml file to be parsed.

        encoding : str, optional
            The encoding used while parsing the pom.xml file. Defaults to UTF-8.

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

    def get(self, key: Union[str, List[str]]) -> Optional[_bs4.element.Tag]:
        """
        Find the element tag based on the provided key, which can be a string
        (separated by dots) or a list of tag names. The result could be a None,
        this means that element are undefined or that users has specified wrong
        element tree path.

        Parameters
        ----------
        key : str or a list of str
            The key representing the element tree path.

        Returns
        -------
        Tag or None :
            A ``bs4.element.Tag`` object representing the desired element tag,
            or ``None`` if the element tag is undefined or cannot be found.

        """

        # Split the key if the key is a string
        keys: List[str] = key.split('.') if isinstance(key, str) else key

        # Find the element according to the first key
        result: _bs4.element.Tag = self.soup.find(keys[0])
        for k in keys[1:]:
            # Break the loop if the result is None
            if not result:
                break
            result = result.find(k)

        return result

    def get_name(self) -> Optional[str]:
        """Return the project name."""
        # => project.name
        name_element: _bs4.element.Tag = self.project_tag.find('name')
        return name_element.text if name_element else name_element

    def get_version(self) -> Optional[str]:
        """Return the project version."""
        # => project.version
        version_element: _bs4.element.Tag = self.project_tag.find('version')
        return version_element.text if version_element else version_element

    def get_id(self) -> Dict[str, Optional[str]]:
        """Return a dictionary with 'groupId' and 'artifactId'."""
        id_element: List[_bs4.element.Tag | None] = [
            self.project_tag.find('groupId'),    # => project.groupId
            self.project_tag.find('artifactId')  # => project.artifactId
        ]

        return {  # Return a dictionary
            'groupId': id_element[0].text if id_element[0] else id_element[0],
            'artifactId': id_element[1].text if id_element[1] else id_element[1]
        }

    def get_url(self) -> Optional[str]:
        """Return the project URL."""
        # => project.url
        url_element: _bs4.element.Tag = self.project_tag.find('url')
        return url_element.text if url_element else url_element

    def get_inception_year(self) -> Optional[str]:
        """Return the project inception year."""
        # => project.inceptionYear
        inc_year_element: _bs4.element.Tag = self.project_tag.find('inceptionYear')
        return inc_year_element.text if inc_year_element else inc_year_element

    def get_author(self) -> Dict[str, Optional[str]]:
        """Return a dictionary with 'id', 'name', and 'url' of the project author."""
        key: str = 'project.developers.developer'
        author_element: List[_bs4.element.Tag | None] = [
            self.get(key + '.id'),    # => project.developers[0].developer.id
            self.get(key + '.name'),  # => project.developers[0].developer.name
            self.get(key + '.url')    # => project.developers[0].developer.url
        ]

        return {  # Return a dictionary
            'id': author_element[0].text if author_element[0] else author_element[0],
            'name': author_element[1].text if author_element[1] else author_element[1],
            'url': author_element[2].text if author_element[2] else author_element[2],
        }

    def get_license(self) -> Dict[str, str]:
        """Return a dictionary with 'name', 'url', and 'distribution' of the project license."""
        key: str = 'project.licenses.license'
        license_element: List[_bs4.element.Tag | None] = [
            self.get(key + '.name'),         # => project.licenses[0].license.name
            self.get(key + '.url'),          # => project.licenses[0].license.url
            self.get(key + '.distribution')  # => project.licenses[0].license.distribution
        ]

        return {
            'name': license_element[0].text if license_element[0] else license_element[0],
            'url': license_element[1].text if license_element[1] else license_element[1],
            'distribution': license_element[2].text if license_element[2] else license_element[2],
        }

    def get_property(self, key: str, dot: bool = True) -> Optional[str]:
        """
        Return the value of the specified property key from the POM properties.

        Parameters
        ----------
        key : str
            The property key.

        dot : bool, optional
            If True, split the key using dots. Defaults to True.

        Returns
        -------
        str or None :
            The property value if found, otherwise, returns None.

        Raises
        ------
        ValueError :
            If the provided key is an empty string or None.

        """
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

        # This way, we can prevent an error due to NoneType use
        result: _bs4.element.Tag = self.get(keys)
        return result.text if result else result


__author__       = AUTHOR
__version__      = VERSION
__version_info__ = VERSION_INFO

# Delete unused variables
del AUTHOR, VERSION, VERSION_INFO
