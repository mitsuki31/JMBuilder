.. Generated with sphinx-quickstart. Sphinx version 5.3.0.

.. meta::
   :description: JMBuilder APIs documentation.
   :keywords: jmbuilder, documentation, jmatrix builder, builder

.. toctree::
   :maxdepth: 4
   :caption: Contents

   api/modules

.. _Ryuu Mitsuki: https://github.com/mitsuki31
.. _Python: https://python.org
.. _Project Repository: https://github.com/mitsuki31/JMBuilder.git

-----

============================
JMBuilder APIs Documentation
============================

**JMBuilder** or **JMatrix Builder**, is a builder that is designed to build and configure the
**JMatrix** library written in Python_ by `Ryuu Mitsuki`_.

For more details about **JMatrix**, you can check out its repository.

    https://github.com/mitsuki31/jmatrix

Usage
=====

Syntax usage::

    $ python -m jmbuilder [OPTIONS]

See Options_ section below, for more details about CLI options. Or you can type::

    $ python -m jmbuilder --help

.. _Options:

Options
=======

+---------------------------------------------+--------------------------------------------------+
|                 Option Name                 |                    Description                   |
+---------------------------------------------+--------------------------------------------------+
| ``-h``, ``--help``                          | Print the help message.                          |
+---------------------------------------------+--------------------------------------------------+
| ``-V``, ``-version``, ``--version``         | Print the version and copyright information.     |
+---------------------------------------------+--------------------------------------------------+
| ``-VV``, ``--only-ver``, ``--only-version`` | Print the version number only.                   |
+---------------------------------------------+--------------------------------------------------+
| ``--fix-mf <pom> <in> [out]``,              | Run the builder to correct the specified         |
| ``--fix-manifest <pom> <in> [out]``         | manifest file containing Maven's variables.      |
|                                             | Utilizes information from the provided POM file. |
+---------------------------------------------+--------------------------------------------------+
| ``--fix-prop <pom> <in> [out]``,            | Run the builder to rectify the specified         |
| ``--fix-properties <pom> <in> [out]``       | properties file with Maven's variables.          |
|                                             | Utilizes information from the provided POM file. |
+---------------------------------------------+--------------------------------------------------+

.. WARNING::
   The builder are not designed to be able to run both options simultaneously, for example::

       $ python -m jmbuilder --fix-mf pom.xml manifest.mf --fix-prop ...

   Attempting with above command will cause an error and program will immediately terminated.
   If you want, just breakdown it into two commands.

Indices and tables
==================

* `Project Repository`_
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

-----

**Last updated on:** |lastupdate|
