# Configuration file for AirGap Deploy documentation

import sys
import os

# Add sphinx-theme submodule to path (local to this repo)
sys.path.insert(0, os.path.abspath('sphinx-theme'))

# Import all shared settings
from theme_config import *

# -- Project information -----------------------------------------------------

project = 'AirGap Deploy'
copyright = '2024, Cleanroom Labs'
author = 'Cleanroom Labs'
version = '0.1.0'
release = '0.1.0'

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

needs_build_needflow = True
needs_flow_show_links = True
needs_flow_link_types = ['links', 'tests', 'implements']
needs_flow_engine = 'graphviz'
needs_id_regex = '^[A-Z0-9_-]{3,}'
needs_extra_options = ['priority']

# -- Intersphinx configuration -----------------------------------------------

# Update intersphinx mapping with cross-project references
intersphinx_mapping.update({
    'airgap-whisper': ('https://cleanroomlabs.dev/docs/airgap-whisper/', None),
    'airgap-transfer': ('https://cleanroomlabs.dev/docs/airgap-transfer/', None),
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
