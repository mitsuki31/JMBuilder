# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('api'))  # Generated APIs docs

project = 'JMBuilder'
copyright = '2023-2024, Ryuu Mitsuki'
author = 'Ryuu Mitsuki'

version = '1.0.0'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinxcontrib.lastupdate',
    'numpydoc'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

autodoc_mock_imports = [
    'typing',
    'bs4'
]

# templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_title = f'{project} v{version}'
html_theme = 'pydata_sphinx_theme'
# html_static_path = ['_static']
