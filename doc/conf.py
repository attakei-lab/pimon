# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from pathlib import Path

import pimon

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = pimon.__name__
copyright = "2022, Kazuya Takei"
author = "Kazuya Takei"
release = pimon.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = []
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
language = "ja"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "bizstyle"
html_static_path = ["_static"]

# -- Options for Manual page output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-manual-page-output
man_pages = [
    (
        f"commands/{src.stem}",
        src.stem,
        "%s %s" % (project, release),
        [author],
        1,
    )
    for src in Path(__file__).parent.glob("commands/*.rst")
]
