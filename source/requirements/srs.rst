Software Requirements Specification
===================================

Introduction
------------

Purpose
~~~~~~~

This Software Requirements Specification (SRS) describes the functional and non-functional requirements for **AirGap Deploy**, a command-line tool for packaging applications and their dependencies for deployment on air-gapped systems.

This document is intended for:

- Developers implementing AirGap Deploy
- Release engineers using AirGap Deploy to package applications
- Technical reviewers evaluating the tool's capabilities

Scope
~~~~~

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Product Name:** AirGap Deploy

**Product Purpose:** Simplify the packaging and installation of software on air-gapped systems

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Benefits:**

- Declarative manifest-based packaging (no custom scripts)
- Cross-platform support (Linux, macOS, Windows)
- Automated dependency collection and vendoring
- Generated installation scripts for air-gapped deployment

**Goals:**

- Enable developers to package any application for air-gap deployment with a single TOML manifest
- Reduce manual effort in preparing air-gap packages from days to minutes
- Ensure reproducible, verifiable deployments

**Out of Scope:**

- GUI interface (CLI only)
- Network-based distribution mechanisms
- Digital signature/verification (future enhancement)
- Automatic updates (contradicts air-gap philosophy)
- Plugin system (deferred to future version)

Definitions, Acronyms, and Abbreviations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-----------------------+--------------------------------------------------------------------+
| Term                  | Definition                                                         |
+=======================+====================================================================+
| **Air-gap**           | Physical isolation from networks, especially the internet          |
+-----------------------+--------------------------------------------------------------------+
| **Component**         | A deployable unit (application, binary, model, package)            |
+-----------------------+--------------------------------------------------------------------+
| **Manifest**          | TOML file defining deployment requirements (``AirGapDeploy.toml``) |
+-----------------------+--------------------------------------------------------------------+
| **Package**           | Final output archive (.tar.gz or .zip) ready for air-gap transfer  |
+-----------------------+--------------------------------------------------------------------+
| **Vendor**            | Process of including all dependencies within a package             |
+-----------------------+--------------------------------------------------------------------+
| **Prep**              | Preparation phase on connected machine                             |
+-----------------------+--------------------------------------------------------------------+
| **Install**           | Installation phase on air-gapped machine                           |
+-----------------------+--------------------------------------------------------------------+
| **TOML**              | Tom’s Obvious Minimal Language (configuration format)              |
+-----------------------+--------------------------------------------------------------------+
| **SHA-256**           | Cryptographic hash function for checksums                          |
+-----------------------+--------------------------------------------------------------------+

Overall Description
-------------------

Product Perspective
~~~~~~~~~~~~~~~~~~~

AirGap Deploy is a **standalone developer tool** that integrates into existing software development workflows. It operates in two distinct phases:

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Phase 1 - Preparation (Connected System):**

- Developer creates ``AirGapDeploy.toml`` manifest
- AirGap Deploy collects application source, dependencies, models, binaries
- Generates deployment package (.tar.gz or .zip)
- Generates installation scripts (install.sh, install.ps1)

**Phase 2 - Installation (Air-Gapped System):**

- User transfers package via USB or other physical media
- User executes generated installation script
- Script builds/installs application from vendored dependencies
- No network access required

**Relationship to Other Systems:**

- **AirGap Transfer:** Optional integration for large packages (see Meta-Architecture_)
- **Cleanroom Whisper:** Reference implementation and primary use case
- **CI/CD pipelines:** Integrates with GitHub Actions, GitLab CI for automated package generation

Product Functions
~~~~~~~~~~~~~~~~~

.. _Meta-Architecture: /docs/meta/meta-architecture.html

AirGap Deploy provides the following major functions:

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Manifest Parsing** - Parse and validate ``AirGapDeploy.toml`` files

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Component Collection** - Download and collect required components:

   - Rust applications with vendored dependencies
   - External binaries from Git repositories
   - Model files from URLs with checksum verification
   - System packages (Linux distributions)

**Packaging** - Create compressed archives with all components

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Install Script Generation** - Generate platform-specific installation scripts

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**CLI Interface** - User-friendly command-line tool with progress reporting

User Characteristics
~~~~~~~~~~~~~~~~~~~~

**Primary Users: Application Developers / Release Engineers**

- **Technical expertise:** High (familiar with command-line tools, build systems)
- **Domain knowledge:** Understands air-gap deployment constraints
- **Frequency of use:** Occasional (during release cycles)
- **Environment:** Development machine with internet access

**Secondary Users: End Users / IT Staff**

- **Technical expertise:** Medium (can run installation scripts)
- **Domain knowledge:** Works with air-gapped systems
- **Frequency of use:** Rare (only during installations/updates)
- **Environment:** Air-gapped production system

Constraints
~~~~~~~~~~~

**Regulatory Constraints:**

- Must comply with open-source licensing (AGPL-3.0)

**Technical Constraints:**

- Requires Rust toolchain for building AirGap Deploy itself
- Preparation phase requires internet access (by design)
- Installation phase must work completely offline
- Package size limited by available storage media

**Design Constraints:**

- Command-line interface only (no GUI)
- Declarative manifest format (TOML)
- Cross-platform compatibility (Linux, macOS, Windows)

Assumptions and Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Assumptions:**

- Developer has internet access during package preparation
- Target air-gapped system has basic build tools (C compiler, make)
- Users can physically transfer files via USB or similar media

**Dependencies:**

- External: Git, cargo, platform-specific package managers
- Rust crates: See :doc:`Roadmap <../roadmap>` (Dependencies Summary) for complete list

Functional Requirements
-----------------------

Manifest Parsing and Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. req:: Parse TOML Manifest Files
   :id: FR-DEPLOY-001
   :status: approved
   :tags: deploy, manifest, parsing
   :priority: must
   :release: v1.0

   The system SHALL parse AirGapDeploy.toml files using TOML syntax.

.. req:: Validate Manifest Structure
   :id: FR-DEPLOY-002
   :status: approved
   :tags: deploy, manifest, validation
   :priority: must
   :release: v1.0

   The system SHALL validate manifest structure and required fields before processing.

.. req:: Support Manifest Sections
   :id: FR-DEPLOY-003
   :status: approved
   :tags: deploy, manifest, structure
   :priority: must
   :release: v1.0

   The system SHALL support the following manifest sections: ``[package]``, ``[targets]``, ``[install]``, ``[[components]]``

.. req:: Clear Manifest Error Messages
   :id: FR-DEPLOY-004
   :status: approved
   :tags: deploy, manifest, validation, error-handling
   :priority: must
   :release: v1.0

   The system SHALL provide clear error messages for invalid manifests, including line numbers and expected values.

.. req:: Manifest Schema Versioning
   :id: FR-DEPLOY-005
   :status: approved
   :tags: deploy, manifest, versioning
   :priority: should
   :release: v1.0

   The system SHALL support schema versioning to enable future manifest evolution.

Component Collection
~~~~~~~~~~~~~~~~~~~~

Rust Application Component
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. req:: Collect Rust Application Source
   :id: FR-DEPLOY-006
   :status: approved
   :tags: deploy, rust, component
   :priority: must
   :release: v1.0

   The system SHALL collect Rust application source code from local directories.

.. req:: Vendor Cargo Dependencies
   :id: FR-DEPLOY-007
   :status: approved
   :tags: deploy, rust, vendor, dependencies
   :priority: must
   :release: v1.0

   The system SHALL execute cargo vendor to download and vendor all Cargo dependencies.

.. req:: Include Rust Toolchain Installer
   :id: FR-DEPLOY-008
   :status: approved
   :tags: deploy, rust, toolchain
   :priority: should
   :release: v1.0

   The system SHALL optionally include Rust toolchain installer for offline builds.

.. req:: Generate Cargo Config
   :id: FR-DEPLOY-009
   :status: approved
   :tags: deploy, rust, configuration
   :priority: must
   :release: v1.0

   The system SHALL generate .cargo/config.toml to configure vendored dependency usage.

.. req:: Rust Component Configuration Options
   :id: FR-DEPLOY-010
   :status: approved
   :tags: deploy, rust, configuration
   :priority: must
   :release: v1.0

   The system SHALL support configuration options: source, vendor, include_toolchain, prebuild

External Binary Component
^^^^^^^^^^^^^^^^^^^^^^^^^

.. req:: Clone Git Repositories
   :id: FR-DEPLOY-011
   :status: approved
   :tags: deploy, git, external-binary
   :priority: must
   :release: v1.0

   The system SHALL clone Git repositories for external binaries.

.. req:: Specify Git Version
   :id: FR-DEPLOY-012
   :status: approved
   :tags: deploy, git, versioning
   :priority: must
   :release: v1.0

   The system SHALL support specifying Git branch, tag, or commit.

.. req:: Include Build Instructions
   :id: FR-DEPLOY-013
   :status: approved
   :tags: deploy, installation, build
   :priority: must
   :release: v1.0

   The system SHALL include build instructions in installation scripts.

.. req:: External Binary Configuration Options
   :id: FR-DEPLOY-014
   :status: approved
   :tags: deploy, external-binary, configuration
   :priority: must
   :release: v1.0

   The system SHALL support configuration options: name, repo, branch/tag/commit, build_instructions

Model File Component
^^^^^^^^^^^^^^^^^^^^

.. req:: Download Model Files
   :id: FR-DEPLOY-015
   :status: approved
   :tags: deploy, model, download
   :priority: must
   :release: v1.0

   The system SHALL download model files from HTTPS URLs.

.. req:: Verify File Checksums
   :id: FR-DEPLOY-016
   :status: approved
   :tags: deploy, model, verification, security
   :priority: must
   :release: v1.0

   The system SHALL verify downloaded files using SHA-256 checksums.

.. req:: Display Download Progress
   :id: FR-DEPLOY-017
   :status: approved
   :tags: deploy, model, download, ui
   :priority: must
   :release: v1.0

   The system SHALL display download progress with progress bars.

.. req:: Resume Interrupted Downloads
   :id: FR-DEPLOY-018
   :status: approved
   :tags: deploy, model, download, reliability
   :priority: should
   :release: v1.0

   The system SHALL support resume capability for interrupted downloads.

.. req:: Model File Configuration Options
   :id: FR-DEPLOY-019
   :status: approved
   :tags: deploy, model, configuration
   :priority: must
   :release: v1.0

   The system SHALL support configuration options: name, url, checksum, required, install_path

System Package Component
^^^^^^^^^^^^^^^^^^^^^^^^

.. req:: Detect Linux Distribution
   :id: FR-DEPLOY-020
   :status: approved
   :tags: deploy, system-package, linux
   :priority: could
   :release: v1.0

   The system SHALL detect Linux distribution (Debian, Fedora, Arch).

.. req:: Download System Packages
   :id: FR-DEPLOY-021
   :status: approved
   :tags: deploy, system-package, dependencies
   :priority: could
   :release: v1.0

   The system SHALL download system packages (.deb, .rpm, etc.) with dependencies.

.. req:: Include System Packages in Archive
   :id: FR-DEPLOY-022
   :status: approved
   :tags: deploy, system-package, packaging
   :priority: could
   :release: v1.0

   The system SHALL include system packages in deployment archive.

.. req:: Configure System Package Installation
   :id: FR-DEPLOY-023
   :status: approved
   :tags: deploy, system-package, installation
   :priority: could
   :release: v1.0

   The system SHALL configure installation scripts to install system packages.

**Note:** SystemPackageComponent is marked as **optional for MVP** and may be deferred.

Packaging
~~~~~~~~~

.. req:: Create Tar.gz Archives
   :id: FR-DEPLOY-024
   :status: approved
   :tags: deploy, packaging, archive
   :priority: must
   :release: v1.0

   The system SHALL create tar.gz archives for Linux and macOS deployments.

.. req:: Create Zip Archives
   :id: FR-DEPLOY-025
   :status: approved
   :tags: deploy, packaging, archive, windows
   :priority: must
   :release: v1.0

   The system SHALL create zip archives for Windows deployments.

.. req:: Organize Package Directory Structure
   :id: FR-DEPLOY-026
   :status: approved
   :tags: deploy, packaging, structure
   :priority: must
   :release: v1.0

   The system SHALL organize package contents with standardized directory structure.

.. req:: Generate Package Metadata
   :id: FR-DEPLOY-027
   :status: approved
   :tags: deploy, packaging, metadata
   :priority: must
   :release: v1.0

   The system SHALL generate airgap-deploy-metadata.json with package information.

.. req:: Generate Package Checksum
   :id: FR-DEPLOY-028
   :status: approved
   :tags: deploy, packaging, verification, security
   :priority: must
   :release: v1.0

   The system SHALL generate SHA-256 checksum for the entire package.

.. req:: Configurable Compression Levels
   :id: FR-DEPLOY-029
   :status: approved
   :tags: deploy, packaging, compression
   :priority: should
   :release: v1.0

   The system SHALL support configurable compression levels.

Installation Script Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. req:: Generate Bash Installation Scripts
   :id: FR-DEPLOY-030
   :status: approved
   :tags: deploy, installation, bash, linux, macos
   :priority: must
   :release: v1.0

   The system SHALL generate Bash installation scripts (install.sh) for Linux/macOS.

.. req:: Generate PowerShell Installation Scripts
   :id: FR-DEPLOY-031
   :status: approved
   :tags: deploy, installation, powershell, windows
   :priority: must
   :release: v1.0

   The system SHALL generate PowerShell installation scripts (install.ps1) for Windows.

.. req:: Installation Script Steps
   :id: FR-DEPLOY-032
   :status: approved
   :tags: deploy, installation, workflow
   :priority: must
   :release: v1.0

   Installation scripts SHALL perform dependency checks, display plan, prompt for location, execute builds, configure files, set permissions, and log actions.

.. req:: Installation Script Modes
   :id: FR-DEPLOY-033
   :status: approved
   :tags: deploy, installation, modes
   :priority: must
   :release: v1.0

   Installation scripts SHALL support interactive mode and automatic (unattended) mode.

.. req:: Detect Existing Installations
   :id: FR-DEPLOY-034
   :status: approved
   :tags: deploy, installation, upgrade
   :priority: should
   :release: v1.0

   Installation scripts SHALL detect existing installations and offer upgrade path.

.. req:: Verify Disk Space
   :id: FR-DEPLOY-035
   :status: approved
   :tags: deploy, installation, validation
   :priority: must
   :release: v1.0

   Installation scripts SHALL verify sufficient disk space before proceeding.

.. req:: Installation Error Messages
   :id: FR-DEPLOY-036
   :status: approved
   :tags: deploy, installation, error-handling
   :priority: must
   :release: v1.0

   Installation scripts SHALL provide clear error messages and recovery instructions.

Command-Line Interface
~~~~~~~~~~~~~~~~~~~~~~

.. req:: CLI Commands
   :id: FR-DEPLOY-037
   :status: approved
   :tags: deploy, cli, commands
   :priority: must
   :release: v1.0

   The system SHALL provide commands: prep, validate, init, list-components with appropriate arguments.

.. req:: Colored CLI Output
   :id: FR-DEPLOY-038
   :status: approved
   :tags: deploy, cli, ui
   :priority: should
   :release: v1.0

   The system SHALL display colored output for improved readability.

.. req:: Progress Bars
   :id: FR-DEPLOY-039
   :status: approved
   :tags: deploy, cli, ui, progress
   :priority: must
   :release: v1.0

   The system SHALL display progress bars for long-running operations (downloads, compression).

.. req:: Verbose Logging Flag
   :id: FR-DEPLOY-040
   :status: approved
   :tags: deploy, cli, logging
   :priority: must
   :release: v1.0

   The system SHALL support --verbose flag for detailed logging.

.. req:: Help Flag
   :id: FR-DEPLOY-041
   :status: approved
   :tags: deploy, cli, help
   :priority: must
   :release: v1.0

   The system SHALL support --help flag for all commands.

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

.. req:: Global Configuration File
   :id: FR-DEPLOY-042
   :status: approved
   :tags: deploy, configuration
   :priority: should
   :release: v1.0

   The system SHALL support global configuration file at ~/.airgap-deploy/config.toml.

.. req:: Global Configuration Options
   :id: FR-DEPLOY-043
   :status: approved
   :tags: deploy, configuration
   :priority: should
   :release: v1.0

   The system SHALL support global configuration options: default_target, cache_dir, proxy.

.. req:: CLI Overrides Configuration
   :id: FR-DEPLOY-044
   :status: approved
   :tags: deploy, configuration, cli
   :priority: must
   :release: v1.0

   Command-line arguments SHALL override global configuration.

Error Handling and Recovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. req:: Clear Error Messages
   :id: FR-DEPLOY-045
   :status: approved
   :tags: deploy, error-handling
   :priority: must
   :release: v1.0

   The system SHALL provide clear, actionable error messages for all failure modes.

.. req:: Suggest Error Recovery Steps
   :id: FR-DEPLOY-046
   :status: approved
   :tags: deploy, error-handling, recovery
   :priority: should
   :release: v1.0

   The system SHALL suggest recovery steps for common errors: missing dependencies, network failures, disk space issues, invalid manifests.

.. req:: Non-Zero Exit Codes
   :id: FR-DEPLOY-047
   :status: approved
   :tags: deploy, error-handling, cli
   :priority: must
   :release: v1.0

   The system SHALL exit with non-zero status codes on errors.

.. req:: Operation Logging
   :id: FR-DEPLOY-048
   :status: approved
   :tags: deploy, logging, debugging
   :priority: must
   :release: v1.0

   The system SHALL log all operations to enable debugging.

Non-Functional Requirements
---------------------------

Performance
~~~~~~~~~~~

.. nfreq:: Package Preparation Performance
   :id: NFR-DEPLOY-001
   :status: approved
   :tags: deploy, performance
   :priority: should
   :release: v1.0

   Package preparation SHALL complete in less than 5 minutes for typical applications (<1GB components).

.. nfreq:: Large Download Handling
   :id: NFR-DEPLOY-002
   :status: approved
   :tags: deploy, performance, download
   :priority: must
   :release: v1.0

   Large model downloads (1-10GB) SHALL display progress and support resume.

.. nfreq:: Parallel Component Collection
   :id: NFR-DEPLOY-003
   :status: approved
   :tags: deploy, performance, parallelism
   :priority: should
   :release: v1.0

   Parallel component collection SHALL be used where possible to reduce preparation time.

.. nfreq:: Installation Performance
   :id: NFR-DEPLOY-004
   :status: approved
   :tags: deploy, performance, installation
   :priority: should
   :release: v1.0

   Installation scripts SHALL complete in less than 20 minutes for typical applications (including build time).

Reliability
~~~~~~~~~~~

.. nfreq:: Checksum Verification
   :id: NFR-DEPLOY-005
   :status: approved
   :tags: deploy, reliability, security, verification
   :priority: must
   :release: v1.0

   The system SHALL verify all downloaded files using SHA-256 checksums.

.. nfreq:: Network Operation Retry
   :id: NFR-DEPLOY-006
   :status: approved
   :tags: deploy, reliability, network
   :priority: must
   :release: v1.0

   The system SHALL retry failed network operations up to 3 times with exponential backoff.

.. nfreq:: Idempotent Installation
   :id: NFR-DEPLOY-007
   :status: approved
   :tags: deploy, reliability, installation
   :priority: must
   :release: v1.0

   Installation scripts SHALL be idempotent (safe to run multiple times).

.. nfreq:: Graceful Interruption Handling
   :id: NFR-DEPLOY-008
   :status: approved
   :tags: deploy, reliability, error-handling
   :priority: must
   :release: v1.0

   The system SHALL handle interruptions gracefully (Ctrl+C, system shutdown).

Usability
~~~~~~~~~

.. nfreq:: First-Time User Experience
   :id: NFR-DEPLOY-009
   :status: approved
   :tags: deploy, usability
   :priority: should
   :release: v1.0

   First-time users SHALL be able to create a deployment package within 10 minutes using provided examples.

.. nfreq:: Detailed Error Messages
   :id: NFR-DEPLOY-010
   :status: approved
   :tags: deploy, usability, error-handling
   :priority: must
   :release: v1.0

   Error messages SHALL include specific details about the failure and suggested fixes.

.. nfreq:: Command Help Text
   :id: NFR-DEPLOY-011
   :status: approved
   :tags: deploy, usability, cli, help
   :priority: must
   :release: v1.0

   The CLI SHALL provide help text accessible via --help for all commands.

.. nfreq:: Progress Indicators
   :id: NFR-DEPLOY-012
   :status: approved
   :tags: deploy, usability, ui
   :priority: must
   :release: v1.0

   Progress indicators SHALL be shown for all operations taking longer than 2 seconds.

Maintainability
~~~~~~~~~~~~~~~

.. nfreq:: Test Coverage
   :id: NFR-DEPLOY-013
   :status: approved
   :tags: deploy, maintainability, testing
   :priority: must
   :release: v1.0

   The codebase SHALL achieve at least 80% test coverage.

.. nfreq:: API Documentation
   :id: NFR-DEPLOY-014
   :status: approved
   :tags: deploy, maintainability, documentation
   :priority: must
   :release: v1.0

   All public APIs SHALL have rustdoc documentation.

.. nfreq:: Clippy Compliance
   :id: NFR-DEPLOY-015
   :status: approved
   :tags: deploy, maintainability, code-quality
   :priority: must
   :release: v1.0

   The code SHALL pass cargo clippy with zero warnings.

.. nfreq:: Code Formatting
   :id: NFR-DEPLOY-016
   :status: approved
   :tags: deploy, maintainability, code-quality
   :priority: must
   :release: v1.0

   The code SHALL be formatted with rustfmt.

Portability
~~~~~~~~~~~

.. nfreq:: Linux Platform Support
   :id: NFR-DEPLOY-017
   :status: approved
   :tags: deploy, portability, linux
   :priority: must
   :release: v1.0

   The system SHALL run on Linux (Ubuntu 20.04+, Fedora 35+, Debian 11+).

.. nfreq:: macOS Platform Support
   :id: NFR-DEPLOY-018
   :status: approved
   :tags: deploy, portability, macos
   :priority: must
   :release: v1.0

   The system SHALL run on macOS (10.15+, both Intel and Apple Silicon).

.. nfreq:: Windows Platform Support
   :id: NFR-DEPLOY-019
   :status: approved
   :tags: deploy, portability, windows
   :priority: must
   :release: v1.0

   The system SHALL run on Windows (Windows 10/11).

.. nfreq:: Installation Script Compatibility
   :id: NFR-DEPLOY-020
   :status: approved
   :tags: deploy, portability, installation
   :priority: must
   :release: v1.0

   Generated installation scripts SHALL be compatible with Bash 4.0+ (Linux/macOS) and PowerShell 5.1+ (Windows).

Security
~~~~~~~~

.. nfreq:: Verify All Checksums
   :id: NFR-DEPLOY-021
   :status: approved
   :tags: deploy, security, verification
   :priority: must
   :release: v1.0

   The system SHALL verify checksums for all downloaded files.

.. nfreq:: No Arbitrary Code Execution
   :id: NFR-DEPLOY-022
   :status: approved
   :tags: deploy, security
   :priority: must
   :release: v1.0

   The system SHALL NOT execute arbitrary code from manifests.

.. nfreq:: Confirm Destructive Operations
   :id: NFR-DEPLOY-023
   :status: approved
   :tags: deploy, security, installation
   :priority: must
   :release: v1.0

   Installation scripts SHALL require explicit confirmation before destructive operations.

.. nfreq:: HTTPS for Network Operations
   :id: NFR-DEPLOY-024
   :status: approved
   :tags: deploy, security, network
   :priority: must
   :release: v1.0

   The system SHALL use HTTPS for all network operations.

.. nfreq:: Restrictive File Permissions
   :id: NFR-DEPLOY-025
   :status: approved
   :tags: deploy, security, filesystem
   :priority: must
   :release: v1.0

   Temporary files SHALL be created with restrictive permissions (user-only).

Scalability
~~~~~~~~~~~

.. nfreq:: Large Package Support
   :id: NFR-DEPLOY-026
   :status: approved
   :tags: deploy, scalability
   :priority: should
   :release: v1.0

   The system SHALL handle packages up to 50GB in size.

.. nfreq:: Multi-Component Manifests
   :id: NFR-DEPLOY-027
   :status: approved
   :tags: deploy, scalability
   :priority: should
   :release: v1.0

   The system SHALL support manifests with up to 100 components.

.. nfreq:: CPU-Scalable Parallelism
   :id: NFR-DEPLOY-028
   :status: approved
   :tags: deploy, scalability, performance
   :priority: should
   :release: v1.0

   Parallel collection SHALL scale with available CPU cores.

.. nfreq:: Platform-Specific Install Paths
   :id: NFR-DEPLOY-029
   :status: approved
   :tags: deploy, portability, installation
   :priority: must
   :release: v1.0

   Install scripts SHALL use platform-specific default paths (user: ~/.local on Linux/macOS, %LOCALAPPDATA% on Windows; system: /usr/local on Linux/macOS, C:\Program Files on Windows)

External Interface Requirements
-------------------------------

User Interfaces
~~~~~~~~~~~~~~~

.. req:: Command-Line Interface with ANSI Color Support
   :id: FR-DEPLOY-049
   :status: approved
   :tags: deploy, external-interface, ui, cli
   :priority: must
   :release: v1.0

   The system SHALL provide a command-line interface with ANSI color support.

.. req:: Progress Bars for Long-Running Operations
   :id: FR-DEPLOY-050
   :status: approved
   :tags: deploy, external-interface, ui, progress
   :priority: must
   :release: v1.0

   The system SHALL display progress bars for long-running operations (using indicatif crate).

.. req:: Interactive Prompts in Installation Scripts
   :id: FR-DEPLOY-051
   :status: approved
   :tags: deploy, external-interface, ui, installation
   :priority: must
   :release: v1.0

   The system SHALL provide interactive prompts in generated installation scripts.

Hardware Interfaces
~~~~~~~~~~~~~~~~~~~

.. req:: Standard Filesystem I/O
   :id: FR-DEPLOY-052
   :status: approved
   :tags: deploy, external-interface, hardware, filesystem
   :priority: must
   :release: v1.0

   The system SHALL use standard filesystem I/O (no special hardware requirements).

.. req:: Network Interface for Component Downloads
   :id: FR-DEPLOY-053
   :status: approved
   :tags: deploy, external-interface, hardware, network
   :priority: must
   :release: v1.0

   The system SHALL use network interface for downloading components during prep phase.

.. req:: Removable Media Support
   :id: FR-DEPLOY-054
   :status: approved
   :tags: deploy, external-interface, hardware, usb
   :priority: must
   :release: v1.0

   The system SHALL support removable media (USB drives) for package transfer (OS-provided).

Software Interfaces
~~~~~~~~~~~~~~~~~~~

.. req:: Cargo Integration for Dependency Vendoring
   :id: FR-DEPLOY-055
   :status: approved
   :tags: deploy, external-interface, software, cargo, rust
   :priority: must
   :release: v1.0

   The system SHALL integrate with ``cargo`` for Rust dependency vendoring.

.. req:: Git Integration for Repository Cloning
   :id: FR-DEPLOY-056
   :status: approved
   :tags: deploy, external-interface, software, git
   :priority: must
   :release: v1.0

   The system SHALL integrate with ``git`` for cloning external repositories.

.. req:: HTTP/HTTPS Clients for Downloads
   :id: FR-DEPLOY-057
   :status: approved
   :tags: deploy, external-interface, software, http
   :priority: must
   :release: v1.0

   The system SHALL use HTTP/HTTPS clients for downloading models and packages.

.. req:: System Package Manager Integration
   :id: FR-DEPLOY-058
   :status: approved
   :tags: deploy, external-interface, software, package-manager
   :priority: should
   :release: v1.0

   The system SHALL integrate with system package managers (apt, dnf, pacman) for SystemPackageComponent.

.. req:: AirGap Transfer Integration
   :id: FR-DEPLOY-059
   :status: approved
   :tags: deploy, external-interface, software, airgap-transfer
   :priority: could
   :release: v1.0

   The system SHALL integrate with AirGap Transfer for large package chunking (workflow level, not code level).

Communications Interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~

.. req:: HTTP/HTTPS for Component Downloads
   :id: FR-DEPLOY-060
   :status: approved
   :tags: deploy, external-interface, communications, http, network
   :priority: must
   :release: v1.0

   The system SHALL use HTTP/HTTPS for downloading components (preparation phase only).

.. req:: No Network During Installation
   :id: FR-DEPLOY-061
   :status: approved
   :tags: deploy, external-interface, communications, air-gap, offline
   :priority: must
   :release: v1.0

   The system SHALL NOT use network communication during installation phase (enforced by air-gap).

Enhanced Installation Features
------------------------------

The following requirements address gaps identified in use case analysis.

Component Selection
~~~~~~~~~~~~~~~~~~~

.. req:: Optional Component Declaration
   :id: FR-DEPLOY-062
   :status: approved
   :tags: deploy, components, configuration
   :priority: should
   :release: v1.0

   Components SHALL support ``required`` field to mark components as optional

.. req:: Component Selection at Prep Time
   :id: FR-DEPLOY-063
   :status: approved
   :tags: deploy, cli, components
   :priority: should
   :release: v1.0

   The CLI SHALL support ``--include`` flag to select optional components during prep

Configuration Generation
~~~~~~~~~~~~~~~~~~~~~~~~~

.. req:: Config File Generation
   :id: FR-DEPLOY-064
   :status: approved
   :tags: deploy, installation, configuration
   :priority: should
   :release: v1.0

   Install scripts SHALL generate configuration files from templates

.. req:: Config Template Support
   :id: FR-DEPLOY-065
   :status: approved
   :tags: deploy, installation, configuration
   :priority: should
   :release: v1.0

   Manifests SHALL support ``[install.config]`` section with ``config_file`` and ``config_template`` fields

.. req:: Custom Installation Steps
   :id: FR-DEPLOY-066
   :status: approved
   :tags: deploy, installation, customization
   :priority: should
   :release: v1.0

   Manifests SHALL support ``[install.steps]`` section for component-specific installation commands

Installation Modes
~~~~~~~~~~~~~~~~~~

.. req:: Interactive Installation Mode
   :id: FR-DEPLOY-067
   :status: approved
   :tags: deploy, installation, usability
   :priority: should
   :release: v1.0

   Install scripts SHALL support interactive mode with user prompts

.. req:: Automatic Installation Mode
   :id: FR-DEPLOY-068
   :status: approved
   :tags: deploy, installation, automation
   :priority: should
   :release: v1.0

   Install scripts SHALL support automatic mode with environment variables (MODE=automatic)

.. req:: Installation Prompts
   :id: FR-DEPLOY-069
   :status: approved
   :tags: deploy, installation, usability
   :priority: could
   :release: v1.0

   Manifests COULD support ``[install.prompts]`` section for interactive prompt configuration

Dependency Management
~~~~~~~~~~~~~~~~~~~~~

.. req:: Dependency Declaration
   :id: FR-DEPLOY-070
   :status: approved
   :tags: deploy, dependencies, configuration
   :priority: should
   :release: v1.0

   Manifests SHALL support ``[install.dependencies]`` section to declare required tools

.. req:: Dependency Verification
   :id: FR-DEPLOY-071
   :status: approved
   :tags: deploy, dependencies, installation
   :priority: must
   :release: v1.0

   Install scripts SHALL verify dependencies before building components

.. req:: Disk Space Verification
   :id: FR-DEPLOY-072
   :status: approved
   :tags: deploy, dependencies, installation
   :priority: should
   :release: v1.0

   Install scripts SHALL verify sufficient disk space before installation

   .. note::

      This requirement covers disk space verification at install time. For disk space verification during the prep phase, see :need:`FR-DEPLOY-035`.

v1.1 — Bill of Materials and Vulnerability Scanning
----------------------------------------------------

The following requirements are planned for v1.1 and are not in scope for the MVP release.

SBOM Generation
~~~~~~~~~~~~~~~

.. req:: Generate CycloneDX SBOM
   :id: FR-DEPLOY-073
   :status: proposed
   :tags: deploy, v1.1, sbom, cyclonedx
   :priority: should
   :release: v1.1

   The system SHALL generate a CycloneDX JSON SBOM during the ``prep`` phase, output alongside the deployment package as ``sbom.cdx.json``.

.. req:: Parse Cargo.lock for Dependency Graph
   :id: FR-DEPLOY-074
   :status: proposed
   :tags: deploy, v1.1, sbom, dependencies
   :priority: should
   :release: v1.1

   The system SHALL parse ``Cargo.lock`` to extract the full transitive dependency graph, including crate names, versions, and dependency relationships.

.. req:: Extract License Information
   :id: FR-DEPLOY-075
   :status: proposed
   :tags: deploy, v1.1, sbom, licensing
   :priority: should
   :release: v1.1

   The system SHALL extract license information for each dependency from ``Cargo.toml`` license fields and include it in the SBOM.

.. req:: Include Component Metadata in SBOM
   :id: FR-DEPLOY-076
   :status: proposed
   :tags: deploy, v1.1, sbom, metadata
   :priority: should
   :release: v1.1

   The SBOM SHALL include component metadata: package name, version, supplier/source URL, and SHA-256 checksums for all collected components.

.. req:: Include SBOM in Deployment Archive
   :id: FR-DEPLOY-077
   :status: proposed
   :tags: deploy, v1.1, sbom, packaging
   :priority: should
   :release: v1.1

   The system SHALL include the generated SBOM in the deployment archive by default.

CBOM Generation
~~~~~~~~~~~~~~~

.. req:: Detect Cryptographic Dependencies
   :id: FR-DEPLOY-078
   :status: proposed
   :tags: deploy, v1.1, cbom, cryptography
   :priority: should
   :release: v1.1

   The system SHALL scan ``Cargo.lock`` for known cryptographic crates (e.g., ring, rustls, aws-lc-rs, openssl-sys, chacha20, aes-gcm, sha2, ed25519-dalek) and record them as CycloneDX CBOM cryptographic asset entries.

.. req:: Document Internal Cryptographic Usage
   :id: FR-DEPLOY-079
   :status: proposed
   :tags: deploy, v1.1, cbom, cryptography
   :priority: should
   :release: v1.1

   The CBOM SHALL document hash algorithms used by AirGap Deploy itself (e.g., SHA-256 for checksum verification).

.. req:: Unified SBOM/CBOM Document
   :id: FR-DEPLOY-080
   :status: proposed
   :tags: deploy, v1.1, sbom, cbom, cyclonedx
   :priority: should
   :release: v1.1

   The CBOM data SHALL be included in the CycloneDX SBOM document as a single unified file, per the CycloneDX specification.

Vulnerability Scanning
~~~~~~~~~~~~~~~~~~~~~~

.. req:: Scan Subcommand
   :id: FR-DEPLOY-081
   :status: proposed
   :tags: deploy, v1.1, vulnerability, cli
   :priority: could
   :release: v1.1

   The system SHALL provide an ``airgap-deploy scan`` subcommand that accepts a CycloneDX SBOM file as input and reports known vulnerabilities.

.. req:: Offline Vulnerability Database
   :id: FR-DEPLOY-082
   :status: proposed
   :tags: deploy, v1.1, vulnerability, offline
   :priority: could
   :release: v1.1

   The scan subcommand SHALL support an offline vulnerability database provided by the user (e.g., a pre-downloaded Grype or Trivy database), requiring no network access.

.. req:: Vulnerability Report Output
   :id: FR-DEPLOY-083
   :status: proposed
   :tags: deploy, v1.1, vulnerability, reporting
   :priority: could
   :release: v1.1

   The scan subcommand SHALL generate vulnerability reports in both JSON (machine-readable) and human-readable formats.

.. req:: Severity Threshold Exit Code
   :id: FR-DEPLOY-084
   :status: proposed
   :tags: deploy, v1.1, vulnerability, cli
   :priority: could
   :release: v1.1

   The scan subcommand SHALL exit with a non-zero status code when vulnerabilities exceed a configurable severity threshold (e.g., ``--fail-on critical``).

v1.0 — Additional Component and Configuration Support
------------------------------------------------------

The following requirements were identified during use case analysis (Ollama deployment) and are included in the v1.0 release.

Config File Component
~~~~~~~~~~~~~~~~~~~~~

.. req:: Config File Component Type
   :id: FR-DEPLOY-085
   :status: approved
   :tags: deploy, component, config-file
   :priority: should
   :release: v1.0

   The system SHALL support a ``config-file`` component type for deploying configuration files (e.g., systemd units, config templates) with inline ``content`` and ``install_path`` fields.

GitHub Release Source
~~~~~~~~~~~~~~~~~~~~~

.. req:: GitHub Release Source Type
   :id: FR-DEPLOY-086
   :status: approved
   :tags: deploy, external-binary, github-release
   :priority: should
   :release: v1.0

   The system SHALL support a ``github-release`` source type for external-binary components, specifying ``repo`` (owner/name), ``tag``, and ``asset_pattern`` (glob pattern for selecting platform-specific release assets).

Extended Install Section
~~~~~~~~~~~~~~~~~~~~~~~~

.. req:: Extended Install Section Fields
   :id: FR-DEPLOY-087
   :status: approved
   :tags: deploy, installation, configuration
   :priority: should
   :release: v1.0

   The system SHALL support ``[install]`` section fields: ``prefix`` (installation root directory), ``user`` (system user for service), ``group`` (system group for service).

Configuration Management Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. req:: Configuration Management Output Format
   :id: FR-DEPLOY-088
   :status: approved
   :tags: deploy, cli, configuration-management
   :priority: could
   :release: v1.0

   The system SHALL support a ``--format`` flag on the ``prep`` command to generate configuration management output (e.g., ``--format ansible`` for Ansible playbooks).

Nested Source Fields
~~~~~~~~~~~~~~~~~~~~

.. req:: Nested Source Field Support
   :id: FR-DEPLOY-089
   :status: approved
   :tags: deploy, manifest, configuration
   :priority: should
   :release: v1.0

   Component configuration SHALL support nested ``source.*`` fields (e.g., ``source.type``, ``source.url``, ``source.checksum``) as an alternative to flat field layout for components with polymorphic source types.

Appendices
----------

Example Manifest
~~~~~~~~~~~~~~~~

.. code:: toml

   [package]
   name = "example-app"
   version = "1.0.0"
   description = "Example application for air-gap deployment"

   [targets]
   platforms = ["linux-x86_64", "macos-aarch64"]
   default = "linux-x86_64"

   [[components]]
   type = "rust-app"
   source = "."
   vendor = true
   include_toolchain = true

   [[components]]
   type = "external-binary"
   name = "dependency"
   repo = "https://github.com/example/dependency.git"
   tag = "v1.0.0"
   build_instructions = "make"

   [[components]]
   type = "model-file"
   name = "model"
   url = "https://example.com/model.bin"
   checksum = "sha256:abc123..."
   required = true

   [install]
   method = "build-from-source"
   install_to = "user"
   mode = "interactive"
