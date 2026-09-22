# Configuration file for the Sphinx documentation builder.

import os
import sys

# -- Project information -----------------------------------------------------

project = "BMW Natural Language Data Analyst"
copyright = "2026, Arul Selvan"
author = "Arul Selvan"
release = "1.0"


# -- General configuration ---------------------------------------------------

extensions = []

templates_path = ["_templates"]

exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]

html_title = "BMW Natural Language Data Analyst"

html_logo = None

html_favicon = None


# -- HTML theme options ------------------------------------------------------

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
}


# -- Language ----------------------------------------------------------------

language = "en"


# -- Source file encoding ----------------------------------------------------

source_suffix = {
    ".rst": "restructuredtext",
}


# -- Master document ---------------------------------------------------------

master_doc = "index"


# -- Build options -----------------------------------------------------------

nitpicky = False