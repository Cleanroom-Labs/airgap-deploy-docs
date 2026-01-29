API Reference
=============

.. note::

   API documentation will be auto-generated from Rust source code once implementation begins.
   This page serves as a placeholder and integration guide for future developers.

Planned Architecture
--------------------

Based on :doc:`../design/sdd`, AirGap Deploy will consist of these modules:

CLI Module (``cli``)
~~~~~~~~~~~~~~~~~~~~

**Purpose:** Command-line interface and argument parsing

**Key Components:**

- ``PrepCommand`` - Main prep command handler
- ``Args`` - Argument parser using clap
- ``TargetPlatform`` - Platform specification

Manifest Module (``manifest``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Parse and validate AirGapDeploy.toml

**Key Components:**

- ``Manifest`` - Main manifest structure
- ``Component`` - Component definitions
- ``ManifestParser`` - TOML parsing and validation

Cargo Module (``cargo``)
~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Rust project analysis and dependency management

**Key Components:**

- ``CargoWorkspace`` - Workspace metadata extraction
- ``DependencyVendor`` - Vendor dependency download
- ``ToolchainManager`` - Rust toolchain bundling

Component Module (``component``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Component type implementations

**Key Components:**

- ``RustAppComponent`` - Rust application handler
- ``ExternalBinaryComponent`` - External binary downloader
- ``ModelFileComponent`` - Model file manager
- ``SystemPackageComponent`` - System package bundler

Package Module (``package``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Archive creation and bundling

**Key Components:**

- ``Packager`` - Main packaging logic
- ``TarBuilder`` - Tar archive creation
- ``Compressor`` - Gzip compression

Installer Module (``installer``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Installation script generation

**Key Components:**

- ``ScriptGenerator`` - Shell script generation
- ``InstallStep`` - Installation step definitions
- ``ConfigTemplate`` - Configuration file templates

Developer Resources
-------------------

See `Rust API Documentation Integration Guide <../../meta/rust-integration-guide.html>`__ for doc comment guidelines, sphinxcontrib-rust configuration, and traceability linking.

Future Enhancements
-------------------

When implementation begins:

- Add ``.. impl::`` directives for each module
- Link implementations to requirements in traceability matrix
- Auto-generate API docs with sphinxcontrib-rust
- Document component trait implementations
- Add workflow examples showing API usage

