AirGap Deploy API Reference
============================

.. note::

   API documentation will be auto-generated from Rust source code once implementation begins.
   This page serves as a placeholder and integration guide for future developers.

Planned Architecture
--------------------

Based on :doc:`/airgap-deploy/design/sdd`, AirGap Deploy will consist of these modules:

CLI Module (``cli``)
~~~~~~~~~~~~~~~~~~~~

**Purpose:** Command-line interface and argument parsing

**Key Components:**

- ``PrepCommand`` - Main prep command handler
- ``Args`` - Argument parser using clap
- ``TargetPlatform`` - Platform specification

**Implements Requirements:** FR-DEPLOY-033, FR-DEPLOY-034, FR-DEPLOY-035

Manifest Module (``manifest``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Parse and validate AirGapDeploy.toml

**Key Components:**

- ``Manifest`` - Main manifest structure
- ``Component`` - Component definitions
- ``ManifestParser`` - TOML parsing and validation

**Implements Requirements:** FR-DEPLOY-001, FR-DEPLOY-002, FR-DEPLOY-003

Cargo Module (``cargo``)
~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Rust project analysis and dependency management

**Key Components:**

- ``CargoWorkspace`` - Workspace metadata extraction
- ``DependencyVendor`` - Vendor dependency download
- ``ToolchainManager`` - Rust toolchain bundling

**Implements Requirements:** FR-DEPLOY-007, FR-DEPLOY-008, FR-DEPLOY-009

Component Module (``component``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Component type implementations

**Key Components:**

- ``RustAppComponent`` - Rust application handler
- ``ExternalBinaryComponent`` - External binary downloader
- ``ModelFileComponent`` - Model file manager
- ``SystemPackageComponent`` - System package bundler

**Implements Requirements:** FR-DEPLOY-004, FR-DEPLOY-010, FR-DEPLOY-013, FR-DEPLOY-016

Package Module (``package``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Archive creation and bundling

**Key Components:**

- ``Packager`` - Main packaging logic
- ``TarBuilder`` - Tar archive creation
- ``Compressor`` - Gzip compression

**Implements Requirements:** FR-DEPLOY-019, FR-DEPLOY-020, FR-DEPLOY-021

Installer Module (``installer``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Installation script generation

**Key Components:**

- ``ScriptGenerator`` - Shell script generation
- ``InstallStep`` - Installation step definitions
- ``ConfigTemplate`` - Configuration file templates

**Implements Requirements:** FR-DEPLOY-025, FR-DEPLOY-026, FR-DEPLOY-027

Integration with Sphinx
------------------------

Rust Doc Comment Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Write doc comments that reference requirements for traceability:

.. code-block:: rust

   /// Parses and validates AirGapDeploy.toml manifest files.
   ///
   /// The manifest defines all components to be bundled in the air-gap
   /// deployment package, including Rust applications, external binaries,
   /// models, and system packages.
   ///
   /// # Implements
   ///
   /// - [`FR-DEPLOY-001`]: Parse AirGapDeploy.toml
   /// - [`FR-DEPLOY-002`]: Validate manifest structure
   /// - [`FR-DEPLOY-003`]: Validate component definitions
   ///
   /// # Example
   ///
   /// ```no_run
   /// use airgap_deploy::manifest::Manifest;
   ///
   /// let manifest = Manifest::from_file("AirGapDeploy.toml")?;
   /// manifest.validate()?;
   /// ```
   pub struct Manifest {
       pub package: PackageInfo,
       pub components: Vec<Component>,
   }

Component Trait Example
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rust

   /// Trait for all component types in deployment packages.
   ///
   /// # Implements
   ///
   /// - [`FR-DEPLOY-004`]: Component type abstraction
   ///
   pub trait ComponentHandler {
       /// Downloads or prepares the component.
       ///
       /// # Implements
       ///
       /// - [`FR-DEPLOY-005`]: Download component files
       ///
       fn prepare(&self, target: &TargetPlatform) -> Result<()>;

       /// Generates installation steps for this component.
       ///
       /// # Implements
       ///
       /// - [`FR-DEPLOY-025`]: Generate installation steps
       ///
       fn install_steps(&self) -> Vec<InstallStep>;
   }

Using sphinxcontrib-rust
~~~~~~~~~~~~~~~~~~~~~~~~

Once code exists, integrate with Sphinx:

**Generate Rust docs:**

   .. code-block:: bash

      cargo doc --no-deps --document-private-items

**Configure sphinxcontrib-rust in conf.py:**

   .. code-block:: python

      extensions = [
          # ... existing extensions
          'sphinxcontrib.rust',
      ]

      rust_crates = {
          'airgap-deploy': '../airgap-deploy',
      }

**Reference Rust items in RST:**

   .. code-block:: rst

      See :rust:struct:`Manifest` for manifest parsing.
      See :rust:trait:`ComponentHandler` for component interface.

**Build documentation:**

   .. code-block:: bash

      cd sphinx-docs
      make html

Traceability Linking
~~~~~~~~~~~~~~~~~~~~

Link implementations back to requirements:

.. code-block:: rst

   .. impl:: Manifest Parser Implementation
      :id: IMPL-DEPLOY-001
      :implements: FR-DEPLOY-001, FR-DEPLOY-002, FR-DEPLOY-003
      :status: planned
      :location: src/manifest/parser.rs

      TOML parsing and validation for AirGapDeploy.toml manifests

Future Enhancements
-------------------

When implementation begins:

Add ``.. impl::`` directives for each module
Link implementations to requirements in traceability matrix
Auto-generate API docs with sphinxcontrib-rust
Document component trait implementations
Add workflow examples showing API usage

See Also
--------

- :doc:`/airgap-deploy/requirements/srs` - Requirements this API implements
- :doc:`/airgap-deploy/design/sdd` - Detailed design specifications
- :doc:`/airgap-deploy/testing/plan` - Test cases validating this API
- :doc:`/airgap-deploy/use-cases/workflow-airgap-whisper` - Real-world usage example
