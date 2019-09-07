# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
#
# SunPy documentation build configuration file.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this file.
#
# All configuration values have a default. Some values are defined in
# the global Astropy configuration which is loaded here before anything else.
# See astropy.sphinx.conf for which values are set there.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('..'))
# IMPORTANT: the above commented section was generated by sphinx-quickstart, but
# is *NOT* appropriate for sunpy or sunpy affiliated packages. It is left
# commented out with this explanation to make it clear why this should not be
# done. If the sys.path entry above is added, when the astropy.sphinx.conf
# import occurs, it will import the *source* version of astropy instead of the
# version installed (if invoked as "make html" or directly with sphinx), or the
# version in the build directory (if "python setup.py build_docs" is used).
# Thus, any C-extensions that are needed to build the documentation will *not*
# be accessible, and the documentation will not build correctly.

import numpy as np
from pkg_resources import get_distribution
import os
import sys
import pathlib
import datetime

# -- Import Base config from sphinx-astropy ------------------------------------
try:
    from sphinx_astropy.conf.v1 import *
except ImportError:
    print('ERROR: the documentation requires the "sphinx-astropy" package to be installed')
    sys.exit(1)

if on_rtd:
    os.environ['SUNPY_CONFIGDIR'] = '/home/docs/'
    os.environ['HOME'] = '/home/docs/'
    os.environ['LANG'] = 'C'
    os.environ['LC_ALL'] = 'C'

versionmod = get_distribution('ndcube')

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
# The short X.Y version.
version = '.'.join(versionmod.version.split('.')[:3])
# The full version, including alpha/beta/rc tags.
release = versionmod.version.split('+')[0]
# Is this version a development release
is_development = '.dev' in release

# -- Shut up numpy warnings from WCSAxes --------------------------------------
np.seterr(invalid='ignore')

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '2.0'

# To perform a Sphinx version check that needs to be more specific than
# major.minor, call `check_sphinx_version("x.y.z")` here.
check_sphinx_version(needs_sphinx)

# Add any custom intersphinx for SunPy
intersphinx_mapping.pop('h5py', None)
intersphinx_mapping['sunpy'] = ('https://docs.sunpy.org/en/stable/', None)
intersphinx_mapping['sqlalchemy'] = ('https://docs.sqlalchemy.org/en/latest/', None)
intersphinx_mapping['pandas'] = ('https://pandas.pydata.org/pandas-docs/stable/', None)
intersphinx_mapping['skimage'] = ('https://scikit-image.org/docs/stable/', None)
intersphinx_mapping['drms'] = ('https://docs.sunpy.org/projects/drms/en/stable/', None)
intersphinx_mapping['parfive'] = ('https://parfive.readthedocs.io/en/latest/', None)

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns.append('_templates')

# Add any paths that contain templates here, relative to this directory.
if 'templates_path' not in locals():  # in case parent conf.py defines it
    templates_path = []
templates_path.append('_templates')

# For the linkcheck
linkcheck_ignore = [r"https://doi.org/\d+",
                    r"https://riot.im/\d+",
                    r"https://github.com/\d+",
                    r"https://docs.sunpy.org/\d+"]
linkcheck_anchors = False

# This is added to the end of RST files - a good place to put substitutions to
# be used globally.
rst_epilog = """
.. ndcube
.. _SunPy: https://sunpy.org
.. _`SunPy mailing list`: https://groups.google.com/group/sunpy
.. _`SunPy dev mailing list`: https://groups.google.com/group/sunpy-dev
"""

# -- Project information ------------------------------------------------------
project = 'ndcube'
author = 'The SunPy Community'
copyright = '{}, {}'.format(datetime.datetime.now().year, author)

try:
    from sunpy_sphinx_theme.conf import *
except ImportError:
    html_theme = 'default'

# The name of an image file (within the static path) to use as favicon of the
# docs. This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "./logo/favicon.ico"

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = f'{project} v{release}'

# Output file base name for HTML help builder.
htmlhelp_basename = project + 'doc'

# A dictionary of values to pass into the template engine’s context for all pages.
html_context = {}
html_context['to_be_indexed'] = ['stable', 'latest']

# -- Options for LaTeX output --------------------------------------------------
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [('index', project + '.tex', project + ' Documentation', author, 'manual')]

# -- Options for manual page output --------------------------------------------
# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [('index', project.lower(), project + ' Documentation', [author], 1)]

# -- Swap to Napoleon ---------------------------------------------------------
# Remove numpydoc
extensions.remove('numpydoc')
extensions.append('sphinx.ext.napoleon')

# Disable having a separate return type row
napoleon_use_rtype = False
# Disable google style docstrings
napoleon_google_docstring = False

extensions += ['sphinx_astropy.ext.edit_on_github', 'sphinx.ext.doctest', 'sphinx.ext.githubpages']

# -- Options for the edit_on_github extension ---------------------------------
# Don't import the module as "version" or it will override the
# "version" configuration parameter
edit_on_github_project = "sunpy/ndcube"
if 'dev' not in release:
    edit_on_github_branch = f"{version}"
else:
    edit_on_github_branch = "master"
edit_on_github_source_root = ""
edit_on_github_doc_root = "docs"
edit_on_github_skip_regex = '_.*|generated/.*'
github_issues_url = 'https://github.com/sunpy/ndcube/issues/'

"""
Write the latest changelog into the documentation.
"""
target_file = os.path.abspath("./whatsnew/latest_changelog.txt")
try:
    from sunpy.util.towncrier import generate_changelog_for_docs
    if is_development:
        generate_changelog_for_docs("../", target_file)
except Exception as e:
    print(f"Failed to add changelog to docs with error {e}.")
# Make sure the file exists or else sphinx will complain.
open(target_file, 'a').close()
