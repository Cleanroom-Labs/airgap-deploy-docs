# Configuration file for AirGap Deploy documentation

import sys
import os

# Add common submodule to path
sys.path.insert(0, os.path.abspath('../common'))

# Import all shared settings
from theme_config import *

# Override default paths from theme_config.py for this project's layout
html_static_path = ['../common/sphinx/_static']
templates_path = ['../common/sphinx/_templates']
html_favicon = '../common/sphinx/_static/favicon.ico'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Project information -----------------------------------------------------

project = 'AirGap Deploy'
copyright = '2024, Cleanroom Labs'
author = 'Cleanroom Labs'
version = get_docs_version()
release = get_docs_version()

# -- Extensions configuration ------------------------------------------------

# Extend shared extensions with project-specific ones
extensions.extend([
    'sphinx.ext.viewcode',
    'sphinx.ext.graphviz',
    'sphinx.ext.todo',
])

# -- sphinx-needs configuration ----------------------------------------------

needs_types = [
    {
        'directive': 'usecase',
        'title': 'Use Case',
        'prefix': 'UC-DEPLOY-',
        'color': '#BFD8D2',
        'style': 'node'
    },
    {
        'directive': 'req',
        'title': 'Requirement',
        'prefix': 'FR-DEPLOY-',
        'color': '#FEDCD2',
        'style': 'node'
    },
    {
        'directive': 'nfreq',
        'title': 'Non-Functional Requirement',
        'prefix': 'NFR-DEPLOY-',
        'color': '#DF744A',
        'style': 'node'
    },
    {
        'directive': 'spec',
        'title': 'Design Specification',
        'prefix': 'DS-DEPLOY-',
        'color': '#DCB239',
        'style': 'node'
    },
    {
        'directive': 'test',
        'title': 'Test Case',
        'prefix': 'TC-DEPLOY-',
        'color': '#84B39D',
        'style': 'node'
    },
]

needs_extra_links = [
    {
        'option': 'tests',
        'incoming': 'is tested by',
        'outgoing': 'tests',
        'copy': False,
        'color': '#84B39D'
    },
    {
        'option': 'implements',
        'incoming': 'is implemented by',
        'outgoing': 'implements',
        'copy': False,
        'color': '#00A8B5'
    },
]

needs_build_json = True
needs_build_needflow = True
needs_flow_show_links = True
needs_flow_link_types = ['links', 'tests', 'implements']
needs_flow_engine = 'graphviz'
needs_id_regex = '^[A-Z0-9_-]{3,}'
needs_extra_options = ['priority']

# -- Intersphinx configuration -----------------------------------------------

# Update intersphinx mapping with cross-project references
intersphinx_mapping.update({
    'cleanroom-whisper': ('https://cleanroomlabs.dev/docs/whisper/', None),
    'airgap-transfer': ('https://cleanroomlabs.dev/docs/transfer/', None),
})

# -- HTML output options -----------------------------------------------------

html_title = 'AirGap Deploy Documentation'
html_short_title = 'AirGap Deploy'

html_context = {
    'display_github': True,
    'github_user': 'cleanroom-labs',
    'github_repo': 'airgap-deploy-docs',
    'github_version': 'main',
    'conf_py_path': '/source/',
}
setup_project_icon(project, html_context)
setup_version_context(html_context)
