Test Plan
=========

Introduction
---------------

Purpose
~~~~~~~

This Test Plan describes the testing strategy, approach, and test cases for **airgap-deploy**, ensuring the tool reliably packages applications for air-gapped deployment.

Scope
~~~~~

**In Scope:**

- Unit tests for all modules
- Integration tests for end-to-end workflows
- Platform-specific tests (Linux, macOS, Windows)
- Performance tests for large packages
- Error handling and recovery tests

**Out of Scope:**

- GUI testing (no GUI in this application)
- Load testing (not a server application)
- Security penetration testing (manual review only)

References
~~~~~~~~~~

- :doc:`Requirements (SRS) <../requirements/srs>`
- :doc:`Design (SDD) <../design/sdd>`
- :doc:`Roadmap <../roadmap>`
- IEEE 829-2008: IEEE Standard for Software Test Documentation

--------------

Test Strategy
----------------

Test Levels
~~~~~~~~~~~

**Unit Testing:**

- Test individual functions and modules in isolation
- Mock external dependencies (filesystem, network)
- Target: 80%+ code coverage

**Integration Testing:**

- Test component interactions
- Test full workflows (manifest → package → install)
- Test on real external resources (Git repos, model files)

**System Testing:**

- Test on actual air-gapped VMs
- Test multi-platform deployments
- Test error recovery scenarios

**Acceptance Testing:**

- Verify requirements satisfaction
- User workflow testing
- Reference implementation (AirGap Whisper deployment)

Test Types
~~~~~~~~~~

=============== ======================== ================
Test Type       Purpose                  Coverage
=============== ======================== ================
**Functional**  Verify requirements      All FR from SRS
**Performance** Verify speed/scalability NFR-1.x from SRS
**Reliability** Verify error handling    NFR-2.x from SRS
**Usability**   Verify UX                NFR-3.x from SRS
**Portability** Verify platforms         NFR-5.x from SRS
**Security**    Verify checksums         NFR-6.x from SRS
=============== ======================== ================

Test Environment
~~~~~~~~~~~~~~~~

**Development Environment:**

- Local development machines (Linux, macOS, Windows)
- Unit tests run on developer machines
- Fast feedback loop

**CI Environment:**

- GitHub Actions with matrix builds
- Ubuntu 20.04, 22.04
- macOS 12, 14
- Windows 10, 11
- Rust stable, beta

**Air-Gapped Environment:**

- VirtualBox/VMware VMs with no network
- Test actual air-gap deployment
- Ubuntu 22.04 VM (primary test target)

--------------

Test Cases
-------------

Manifest Parsing (FR-1.x)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Valid Manifest Parsing
   :id: TC-MAN-001
   :status: approved
   :tags: deploy, manifest, parsing
   :tests: FR-DEPLOY-001
   :priority: high

   Verify valid AirGapDeploy.toml parses successfully

.. test:: Invalid Manifest - Missing Required Field
   :id: TC-MAN-002
   :status: approved
   :tags: deploy, manifest, validation, error-handling
   :tests: FR-DEPLOY-002, FR-DEPLOY-004
   :priority: high

   Verify parse error when required field missing

.. test:: Invalid Manifest - Wrong Type
   :id: TC-MAN-003
   :status: approved
   :tags: deploy, manifest, validation, error-handling
   :tests: FR-DEPLOY-002, FR-DEPLOY-004
   :priority: high

   Verify parse error on type mismatch

.. test:: Unsupported Component Type
   :id: TC-MAN-004
   :status: approved
   :tags: deploy, manifest, validation, component
   :tests: FR-DEPLOY-002, FR-DEPLOY-004
   :priority: medium

   Verify validation error for unknown component type

.. test:: Schema Versioning
   :id: TC-MAN-005
   :status: approved
   :tags: deploy, manifest, versioning
   :tests: FR-DEPLOY-005
   :priority: low

   Verify warning for future schema version

--------------

RustAppComponent (FR-2.1 to FR-2.5)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Rust App with Vendoring
   :id: TC-RUST-001
   :status: approved
   :tags: deploy, rust, vendor
   :tests: FR-DEPLOY-007, FR-DEPLOY-009
   :priority: high

   Verify cargo vendor and config generation

.. test:: Rust Toolchain Inclusion
   :id: TC-RUST-002
   :status: approved
   :tags: deploy, rust, toolchain
   :tests: FR-DEPLOY-008
   :priority: medium

   Verify Rust installer download and inclusion

.. test:: Missing Cargo.toml
   :id: TC-RUST-003
   :status: approved
   :tags: deploy, rust, error-handling
   :tests: FR-DEPLOY-006, FR-DEPLOY-045
   :priority: medium

   Verify error when Cargo.toml not found

.. test:: Cargo Vendor Failure
   :id: TC-RUST-004
   :status: approved
   :tags: deploy, rust, vendor, error-handling
   :tests: FR-DEPLOY-007, FR-DEPLOY-045
   :priority: medium

   Verify error handling for cargo vendor failures

--------------

ExternalBinaryComponent (FR-2.6 to FR-2.9)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Git Repository Cloning
   :id: TC-GIT-001
   :status: approved
   :tags: deploy, git, clone
   :tests: FR-DEPLOY-011, FR-DEPLOY-012
   :priority: high

   Verify Git repository cloning with tag checkout

.. test:: Git Branch Checkout
   :id: TC-GIT-002
   :status: approved
   :tags: deploy, git, branch
   :tests: FR-DEPLOY-012
   :priority: high

   Verify Git branch checkout

.. test:: Invalid Repository URL
   :id: TC-GIT-003
   :status: approved
   :tags: deploy, git, error-handling
   :tests: FR-DEPLOY-011, FR-DEPLOY-045
   :priority: medium

   Verify error for invalid repository URL

.. test:: Network Failure During Clone
   :id: TC-GIT-004
   :status: approved
   :tags: deploy, git, network, reliability
   :tests: NFR-DEPLOY-006, FR-DEPLOY-045
   :priority: high

   Verify retry logic for network failures

--------------

ModelFileComponent (FR-2.10 to FR-2.14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Model File Download
   :id: TC-MODEL-001
   :status: approved
   :tags: deploy, model, download
   :tests: FR-DEPLOY-015, FR-DEPLOY-016
   :priority: high

   Verify model file download with checksum verification

.. test:: Checksum Verification Success
   :id: TC-MODEL-002
   :status: approved
   :tags: deploy, model, verification, security
   :tests: FR-DEPLOY-016, NFR-DEPLOY-005
   :priority: high

   Verify checksum verification passes for matching checksum

.. test:: Checksum Verification Failure
   :id: TC-MODEL-003
   :status: approved
   :tags: deploy, model, verification, security, error-handling
   :tests: FR-DEPLOY-016, NFR-DEPLOY-005, FR-DEPLOY-045
   :priority: high

   Verify error and file deletion on checksum mismatch

.. test:: Download Resume
   :id: TC-MODEL-004
   :status: approved
   :tags: deploy, model, download, reliability
   :tests: FR-DEPLOY-018
   :priority: medium

   Verify download resume capability

.. test:: Large File Download
   :id: TC-MODEL-005
   :status: approved
   :tags: deploy, model, download, performance
   :tests: FR-DEPLOY-017, NFR-DEPLOY-002
   :priority: high

   Verify large file download with progress display

.. test:: Download Cache Hit
   :id: TC-MODEL-006
   :status: approved
   :tags: deploy, model, cache, performance
   :tests: FR-DEPLOY-016
   :priority: medium

   Verify cached file reuse

--------------

Packaging (FR-3.1 to FR-3.6)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Create tar.gz Package
   :id: TC-PKG-001
   :status: approved
   :tags: deploy, packaging, archive, linux, macos
   :tests: FR-DEPLOY-024, FR-DEPLOY-026
   :priority: high

   Verify tar.gz archive creation with correct structure

.. test:: Create zip Package
   :id: TC-PKG-002
   :status: approved
   :tags: deploy, packaging, archive, windows
   :tests: FR-DEPLOY-025, FR-DEPLOY-026
   :priority: high

   Verify zip archive creation for Windows

.. test:: Package Metadata Generation
   :id: TC-PKG-003
   :status: approved
   :tags: deploy, packaging, metadata
   :tests: FR-DEPLOY-027
   :priority: high

   Verify metadata file generation

.. test:: Package Checksum Generation
   :id: TC-PKG-004
   :status: approved
   :tags: deploy, packaging, checksum, security
   :tests: FR-DEPLOY-028, NFR-DEPLOY-005
   :priority: high

   Verify package checksum generation

.. test:: Large Package Creation
   :id: TC-PKG-005
   :status: approved
   :tags: deploy, packaging, performance, scalability
   :tests: NFR-DEPLOY-026
   :priority: medium

   Verify large package creation with stable memory usage

--------------

Install Script Generation (FR-4.1 to FR-4.7)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Bash Script Generation
   :id: TC-INSTALL-001
   :status: approved
   :tags: deploy, installation, bash, linux, macos
   :tests: FR-DEPLOY-030, FR-DEPLOY-032
   :priority: high

   Verify Bash installation script generation

.. test:: PowerShell Script Generation
   :id: TC-INSTALL-002
   :status: approved
   :tags: deploy, installation, powershell, windows
   :tests: FR-DEPLOY-031, FR-DEPLOY-032
   :priority: high

   Verify PowerShell installation script generation

.. test:: Interactive Mode Prompts
   :id: TC-INSTALL-003
   :status: approved
   :tags: deploy, installation, interactive
   :tests: FR-DEPLOY-033
   :priority: high

   Verify interactive mode prompts user

.. test:: Automatic Mode
   :id: TC-INSTALL-004
   :status: approved
   :tags: deploy, installation, automatic
   :tests: FR-DEPLOY-033
   :priority: high

   Verify automatic unattended installation

.. test:: Dependency Check Success
   :id: TC-INSTALL-005
   :status: approved
   :tags: deploy, installation, dependencies
   :tests: FR-DEPLOY-032
   :priority: high

   Verify dependency check passes when all present

.. test:: Dependency Check Failure
   :id: TC-INSTALL-006
   :status: approved
   :tags: deploy, installation, dependencies, error-handling
   :tests: FR-DEPLOY-032, FR-DEPLOY-036
   :priority: high

   Verify clear error message for missing dependencies

--------------

CLI Interface (FR-5.1 to FR-5.5)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Prep Command - Default Manifest
   :id: TC-CLI-001
   :status: approved
   :tags: deploy, cli, prep
   :tests: FR-DEPLOY-037
   :priority: high

   Verify prep command with default manifest

.. test:: Prep Command - Custom Manifest
   :id: TC-CLI-002
   :status: approved
   :tags: deploy, cli, prep
   :tests: FR-DEPLOY-037
   :priority: high

   Verify prep command with custom manifest path

.. test:: Prep Command - Dry Run
   :id: TC-CLI-003
   :status: approved
   :tags: deploy, cli, prep, dry-run
   :tests: FR-DEPLOY-037
   :priority: medium

   Verify dry run mode shows plan without executing

.. test:: Validate Command
   :id: TC-CLI-004
   :status: approved
   :tags: deploy, cli, validate
   :tests: FR-DEPLOY-037
   :priority: high

   Verify validate command checks manifest

.. test:: Init Command
   :id: TC-CLI-005
   :status: approved
   :tags: deploy, cli, init
   :tests: FR-DEPLOY-037
   :priority: medium

   Verify init command creates template

.. test:: List Components Command
   :id: TC-CLI-006
   :status: approved
   :tags: deploy, cli, list
   :tests: FR-DEPLOY-037
   :priority: low

   Verify list-components command displays available types

.. test:: Help Flag
   :id: TC-CLI-007
   :status: approved
   :tags: deploy, cli, help
   :tests: FR-DEPLOY-041
   :priority: high

   Verify --help flag displays usage information

--------------

Error Handling (FR-7.1 to FR-7.4)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Network Error with Retry
   :id: TC-ERR-001
   :status: approved
   :tags: deploy, error-handling, network, reliability
   :tests: NFR-DEPLOY-006, FR-DEPLOY-046
   :priority: high

   Verify retry logic for network errors

.. test:: Disk Space Error
   :id: TC-ERR-002
   :status: approved
   :tags: deploy, error-handling, disk-space
   :tests: FR-DEPLOY-035, FR-DEPLOY-045
   :priority: high

   Verify clear error for insufficient disk space

.. test:: Permission Error
   :id: TC-ERR-003
   :status: approved
   :tags: deploy, error-handling, permissions
   :tests: FR-DEPLOY-045
   :priority: medium

   Verify clear error for permission issues

.. test:: Invalid Platform
   :id: TC-ERR-004
   :status: approved
   :tags: deploy, error-handling, platform
   :tests: FR-DEPLOY-045
   :priority: medium

   Verify error for invalid platform target

--------------

End-to-End Workflows
~~~~~~~~~~~~~~~~~~~~

.. test:: AirGap Whisper End-to-End Deployment
   :id: TC-E2E-001
   :status: approved
   :tags: deploy, e2e, airgap-whisper, system
   :tests: UC-DEPLOY-001
   :priority: critical

   Verify complete AirGap Whisper deployment workflow from package creation to functional installation on air-gapped system

.. test:: Ollama Large Model Deployment
   :id: TC-E2E-002
   :status: approved
   :tags: deploy, e2e, ollama, large-package, system
   :tests: UC-DEPLOY-002, NFR-DEPLOY-026
   :priority: high

   Verify Ollama deployment with multiple large models (20GB+ total)

.. test:: Multi-Platform Build
   :id: TC-E2E-003
   :status: approved
   :tags: deploy, e2e, multi-platform, portability
   :tests: NFR-DEPLOY-017, NFR-DEPLOY-018, NFR-DEPLOY-019
   :priority: high

   Verify same manifest builds packages for all platforms

--------------

Performance Tests
~~~~~~~~~~~~~~~~~

.. test:: Package Preparation Time
   :id: TC-PERF-001
   :status: approved
   :tags: deploy, performance, packaging
   :tests: NFR-DEPLOY-001
   :priority: medium

   Verify package preparation completes within 5 minutes for typical applications

.. test:: Large Model Download Performance
   :id: TC-PERF-002
   :status: approved
   :tags: deploy, performance, download, memory
   :tests: NFR-DEPLOY-002
   :priority: high

   Verify large model download with progress display and low memory usage

.. test:: Parallel Component Collection
   :id: TC-PERF-003
   :status: approved
   :tags: deploy, performance, parallelism
   :tests: NFR-DEPLOY-003
   :priority: medium

   Verify parallel collection improves performance

.. test:: Installation Script Performance
   :id: TC-PERF-004
   :status: approved
   :tags: deploy, performance, installation
   :tests: NFR-DEPLOY-004
   :priority: medium

   Verify installation completes within 20 minutes

--------------

Security Tests
~~~~~~~~~~~~~~

.. test:: Checksum Verification Prevents Corruption
   :id: TC-DEPLOY-SEC-001
   :status: approved
   :tags: deploy, security, checksum, verification
   :tests: NFR-DEPLOY-021
   :priority: critical

   Verify checksum verification detects corrupted files

.. test:: No Arbitrary Code Execution
   :id: TC-DEPLOY-SEC-002
   :status: approved
   :tags: deploy, security, code-execution
   :tests: NFR-DEPLOY-022
   :priority: critical

   Verify manifest cannot execute arbitrary code during prep phase

.. test:: HTTPS for Downloads
   :id: TC-DEPLOY-SEC-003
   :status: approved
   :tags: deploy, security, network, https
   :tests: NFR-DEPLOY-024
   :priority: high

   Verify all downloads use HTTPS

.. test:: Temporary File Permissions
   :id: TC-DEPLOY-SEC-004
   :status: approved
   :tags: deploy, security, permissions, filesystem
   :tests: NFR-DEPLOY-025
   :priority: high

   Verify temporary files have restrictive permissions

Enhanced Installation Feature Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Optional Component Declaration
   :id: TC-DEPLOY-INST-001
   :status: approved
   :tags: deploy, components, configuration
   :tests: FR-DEPLOY-062
   :priority: medium

   Verify manifest supports required=false for optional components

.. test:: Component Selection with --include Flag
   :id: TC-DEPLOY-INST-002
   :status: approved
   :tags: deploy, cli, components
   :tests: FR-DEPLOY-063
   :priority: medium

   Verify --include flag selects optional components during prep

.. test:: Config File Generation from Template
   :id: TC-DEPLOY-INST-003
   :status: approved
   :tags: deploy, installation, configuration
   :tests: FR-DEPLOY-064
   :priority: high

   Verify install script generates config file from template with variable substitution

.. test:: Config Template in Manifest
   :id: TC-DEPLOY-INST-004
   :status: approved
   :tags: deploy, installation, configuration
   :tests: FR-DEPLOY-065
   :priority: high

   Verify [install.config] section supports config_file and config_template fields

.. test:: Custom Installation Steps Execution
   :id: TC-DEPLOY-INST-005
   :status: approved
   :tags: deploy, installation, customization
   :tests: FR-DEPLOY-066
   :priority: high

   Verify [install.steps] section commands execute in correct order

.. test:: Interactive Installation Mode
   :id: TC-DEPLOY-INST-006
   :status: approved
   :tags: deploy, installation, usability
   :tests: FR-DEPLOY-067
   :priority: medium

   Verify install script prompts user in interactive mode

.. test:: Automatic Installation Mode
   :id: TC-DEPLOY-INST-007
   :status: approved
   :tags: deploy, installation, automation
   :tests: FR-DEPLOY-068
   :priority: high

   Verify install script runs without prompts when MODE=automatic

.. test:: Installation Prompt Configuration
   :id: TC-DEPLOY-INST-008
   :status: approved
   :tags: deploy, installation, usability
   :tests: FR-DEPLOY-069
   :priority: low

   Verify [install.prompts] section configures interactive prompts

.. test:: Dependency Declaration in Manifest
   :id: TC-DEPLOY-INST-009
   :status: approved
   :tags: deploy, dependencies, configuration
   :tests: FR-DEPLOY-070
   :priority: medium

   Verify [install.dependencies] section declares required tools

.. test:: Dependency Verification Before Build
   :id: TC-DEPLOY-INST-010
   :status: approved
   :tags: deploy, dependencies, installation
   :tests: FR-DEPLOY-071
   :priority: high

   Verify install script checks for required dependencies and fails early if missing

.. test:: Disk Space Verification
   :id: TC-DEPLOY-INST-011
   :status: approved
   :tags: deploy, dependencies, installation
   :tests: FR-DEPLOY-072
   :priority: medium

   Verify install script checks available disk space before installation

.. test:: Platform-Specific Install Paths
   :id: TC-DEPLOY-INST-012
   :status: approved
   :tags: deploy, portability, installation
   :tests: NFR-DEPLOY-029
   :priority: high

   Verify install script uses platform-specific default paths on Linux, macOS, Windows

--------------

Component Configuration Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Rust Component Configuration Options
   :id: TC-DEPLOY-CFG-001
   :status: approved
   :tags: deploy, rust, configuration
   :tests: FR-DEPLOY-010
   :priority: high

   Verify Rust component supports source, vendor, include_toolchain, prebuild config options

.. test:: External Binary Configuration Options
   :id: TC-DEPLOY-CFG-002
   :status: approved
   :tags: deploy, external-binary, configuration
   :tests: FR-DEPLOY-014
   :priority: high

   Verify external binary supports name, repo, branch/tag/commit, build_instructions config options

.. test:: Model File Configuration Options
   :id: TC-DEPLOY-CFG-003
   :status: approved
   :tags: deploy, model, configuration
   :tests: FR-DEPLOY-019
   :priority: high

   Verify model file supports name, url, checksum, required, install_path config options

--------------

System Package Component Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Linux Distribution Detection
   :id: TC-DEPLOY-SYSPKG-001
   :status: approved
   :tags: deploy, system-package, linux
   :tests: FR-DEPLOY-020
   :priority: medium

   Verify system detects Linux distribution (Debian, Fedora, Arch)

.. test:: System Package Installation Configuration
   :id: TC-DEPLOY-SYSPKG-002
   :status: approved
   :tags: deploy, system-package, installation
   :tests: FR-DEPLOY-023
   :priority: medium

   Verify install scripts configure system package installation commands

--------------

Installation Detection Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Existing Installation Detection
   :id: TC-DEPLOY-UPG-001
   :status: approved
   :tags: deploy, installation, upgrade
   :tests: FR-DEPLOY-034
   :priority: high

   Verify install script detects existing installation and offers upgrade path

--------------

CLI Feature Tests
~~~~~~~~~~~~~~~~~

.. test:: Colored CLI Output
   :id: TC-DEPLOY-CLI-001
   :status: approved
   :tags: deploy, cli, ui
   :tests: FR-DEPLOY-038
   :priority: medium

   Verify CLI displays colored output using ANSI codes

.. test:: Progress Bars for Long Operations
   :id: TC-DEPLOY-CLI-002
   :status: approved
   :tags: deploy, cli, ui, progress
   :tests: FR-DEPLOY-039, FR-DEPLOY-050
   :priority: high

   Verify progress bars display for downloads and compression operations

.. test:: Verbose Logging Flag
   :id: TC-DEPLOY-CLI-003
   :status: approved
   :tags: deploy, cli, logging
   :tests: FR-DEPLOY-040, FR-DEPLOY-048
   :priority: high

   Verify --verbose flag enables detailed operation logging

--------------

Configuration Management Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Global Configuration File
   :id: TC-DEPLOY-GLOBALCFG-001
   :status: approved
   :tags: deploy, configuration
   :tests: FR-DEPLOY-042
   :priority: medium

   Verify system reads configuration from ~/.airgap-deploy/config.toml

.. test:: Global Configuration Options
   :id: TC-DEPLOY-GLOBALCFG-002
   :status: approved
   :tags: deploy, configuration
   :tests: FR-DEPLOY-043
   :priority: medium

   Verify global config supports default_target, cache_dir, proxy options

.. test:: CLI Overrides Configuration
   :id: TC-DEPLOY-GLOBALCFG-003
   :status: approved
   :tags: deploy, configuration, cli
   :tests: FR-DEPLOY-044
   :priority: high

   Verify command-line arguments override global configuration values

--------------

Error Handling Tests
~~~~~~~~~~~~~~~~~~~~

.. test:: Non-Zero Exit Codes on Errors
   :id: TC-DEPLOY-ERR-005
   :status: approved
   :tags: deploy, error-handling, cli
   :tests: FR-DEPLOY-047
   :priority: high

   Verify system exits with non-zero status codes on errors

.. test:: Operation Logging for Debugging
   :id: TC-DEPLOY-ERR-006
   :status: approved
   :tags: deploy, logging, debugging
   :tests: FR-DEPLOY-048
   :priority: medium

   Verify all operations are logged to enable debugging

--------------

External Interface Tests
~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: CLI with ANSI Color Support
   :id: TC-DEPLOY-EXTIF-001
   :status: approved
   :tags: deploy, external-interface, ui, cli
   :tests: FR-DEPLOY-049
   :priority: medium

   Verify CLI provides ANSI color support for terminal output

.. test:: Interactive Prompts in Install Scripts
   :id: TC-DEPLOY-EXTIF-002
   :status: approved
   :tags: deploy, external-interface, ui, installation
   :tests: FR-DEPLOY-051
   :priority: high

   Verify generated install scripts provide interactive prompts

.. test:: Standard Filesystem I/O
   :id: TC-DEPLOY-EXTIF-003
   :status: approved
   :tags: deploy, external-interface, hardware, filesystem
   :tests: FR-DEPLOY-052
   :priority: low

   Verify system uses standard filesystem I/O operations

.. test:: Network Interface for Downloads
   :id: TC-DEPLOY-EXTIF-004
   :status: approved
   :tags: deploy, external-interface, hardware, network
   :tests: FR-DEPLOY-053, FR-DEPLOY-060
   :priority: medium

   Verify system uses network interface for component downloads during prep phase

.. test:: Removable Media Support
   :id: TC-DEPLOY-EXTIF-005
   :status: approved
   :tags: deploy, external-interface, hardware, usb
   :tests: FR-DEPLOY-054
   :priority: medium

   Verify packages can be transferred via removable media (USB drives)

.. test:: Cargo Integration
   :id: TC-DEPLOY-EXTIF-006
   :status: approved
   :tags: deploy, external-interface, software, cargo, rust
   :tests: FR-DEPLOY-055
   :priority: high

   Verify integration with cargo for Rust dependency vendoring

.. test:: Git Integration
   :id: TC-DEPLOY-EXTIF-007
   :status: approved
   :tags: deploy, external-interface, software, git
   :tests: FR-DEPLOY-056
   :priority: high

   Verify integration with git for repository cloning

.. test:: HTTP/HTTPS Client Downloads
   :id: TC-DEPLOY-EXTIF-008
   :status: approved
   :tags: deploy, external-interface, software, http
   :tests: FR-DEPLOY-057
   :priority: high

   Verify HTTP/HTTPS clients download models and packages

.. test:: System Package Manager Integration
   :id: TC-DEPLOY-EXTIF-009
   :status: approved
   :tags: deploy, external-interface, software, package-manager
   :tests: FR-DEPLOY-058
   :priority: medium

   Verify integration with apt, dnf, pacman for system packages

.. test:: AirGap Transfer Workflow Integration
   :id: TC-DEPLOY-EXTIF-010
   :status: approved
   :tags: deploy, external-interface, software, airgap-transfer
   :tests: FR-DEPLOY-059
   :priority: low

   Verify workflow-level integration with airgap-transfer for large packages

.. test:: No Network During Installation
   :id: TC-DEPLOY-EXTIF-011
   :status: approved
   :tags: deploy, external-interface, communications, air-gap, offline
   :tests: FR-DEPLOY-061
   :priority: critical

   Verify installation phase uses no network communication (enforced by air-gap)

--------------

Reliability NFR Tests
~~~~~~~~~~~~~~~~~~~~~

.. test:: Idempotent Installation
   :id: TC-DEPLOY-NFR-001
   :status: approved
   :tags: deploy, reliability, installation
   :tests: NFR-DEPLOY-007
   :priority: high

   Verify install scripts can be run multiple times safely without side effects

.. test:: Graceful Interruption Handling
   :id: TC-DEPLOY-NFR-002
   :status: approved
   :tags: deploy, reliability, error-handling
   :tests: NFR-DEPLOY-008
   :priority: high

   Verify system handles Ctrl+C and system shutdown gracefully

--------------

Usability NFR Tests
~~~~~~~~~~~~~~~~~~~

.. test:: First-Time User Experience
   :id: TC-DEPLOY-NFR-003
   :status: approved
   :tags: deploy, usability
   :tests: NFR-DEPLOY-009
   :priority: medium

   Verify first-time users can create deployment package within 10 minutes using examples

.. test:: Detailed Error Messages
   :id: TC-DEPLOY-NFR-004
   :status: approved
   :tags: deploy, usability, error-handling
   :tests: NFR-DEPLOY-010
   :priority: high

   Verify error messages include specific details and suggested fixes

.. test:: Command Help Text
   :id: TC-DEPLOY-NFR-005
   :status: approved
   :tags: deploy, usability, cli, help
   :tests: NFR-DEPLOY-011
   :priority: high

   Verify CLI provides help text via --help for all commands

.. test:: Progress Indicators for Long Operations
   :id: TC-DEPLOY-NFR-006
   :status: approved
   :tags: deploy, usability, ui
   :tests: NFR-DEPLOY-012
   :priority: medium

   Verify progress indicators show for operations taking longer than 2 seconds

--------------

Maintainability NFR Tests
~~~~~~~~~~~~~~~~~~~~~~~~~

.. test:: Test Coverage Requirement
   :id: TC-DEPLOY-NFR-007
   :status: approved
   :tags: deploy, maintainability, testing
   :tests: NFR-DEPLOY-013
   :priority: high

   Verify codebase achieves at least 80% test coverage

.. test:: API Documentation Requirement
   :id: TC-DEPLOY-NFR-008
   :status: approved
   :tags: deploy, maintainability, documentation
   :tests: NFR-DEPLOY-014
   :priority: high

   Verify all public APIs have rustdoc documentation

.. test:: Clippy Compliance
   :id: TC-DEPLOY-NFR-009
   :status: approved
   :tags: deploy, maintainability, code-quality
   :tests: NFR-DEPLOY-015
   :priority: high

   Verify code passes cargo clippy with zero warnings

.. test:: Code Formatting
   :id: TC-DEPLOY-NFR-010
   :status: approved
   :tags: deploy, maintainability, code-quality
   :tests: NFR-DEPLOY-016
   :priority: high

   Verify code is formatted with rustfmt

--------------

Portability NFR Tests
~~~~~~~~~~~~~~~~~~~~~

.. test:: Installation Script Compatibility
   :id: TC-DEPLOY-NFR-011
   :status: approved
   :tags: deploy, portability, installation
   :tests: NFR-DEPLOY-020
   :priority: high

   Verify install scripts are compatible with Bash 4.0+ and PowerShell 5.1+

--------------

Security NFR Tests
~~~~~~~~~~~~~~~~~~

.. test:: Confirm Destructive Operations
   :id: TC-DEPLOY-NFR-012
   :status: approved
   :tags: deploy, security, installation
   :tests: NFR-DEPLOY-023
   :priority: critical

   Verify install scripts require explicit confirmation before destructive operations

--------------

Scalability NFR Tests
~~~~~~~~~~~~~~~~~~~~~

.. test:: Multi-Component Manifest Support
   :id: TC-DEPLOY-NFR-013
   :status: approved
   :tags: deploy, scalability
   :tests: NFR-DEPLOY-027
   :priority: medium

   Verify system supports manifests with up to 100 components

.. test:: CPU-Scalable Parallelism
   :id: TC-DEPLOY-NFR-014
   :status: approved
   :tags: deploy, scalability, performance
   :tests: NFR-DEPLOY-028
   :priority: medium

   Verify parallel collection scales with available CPU cores

--------------

Test Execution
-----------------

Unit Tests
~~~~~~~~~~

.. code:: bash

   # Run all unit tests
   cargo test --lib

   # Run with coverage
   cargo tarpaulin --out Html

   # Target: 80%+ coverage

Integration Tests
~~~~~~~~~~~~~~~~~

.. code:: bash

   # Run integration tests
   cargo test --test '*'

   # Run specific integration test
   cargo test --test e2e_whisper_deployment

CI/CD Testing
~~~~~~~~~~~~~

.. code:: yaml

   # .github/workflows/test.yml
   name: Tests

   on: [push, pull_request]

   jobs:
     test:
       strategy:
         matrix:
           os: [ubuntu-latest, macos-latest, windows-latest]
           rust: [stable, beta]
       runs-on: ${{ matrix.os }}
       steps:
         - uses: actions/checkout@v4
         - uses: dtolnay/rust-toolchain@${{ matrix.rust }}
         - run: cargo test --all-features
         - run: cargo clippy -- -D warnings
         - run: cargo fmt --check

Air-Gapped VM Testing
~~~~~~~~~~~~~~~~~~~~~

**Setup:**

.. code:: bash

   # Create Ubuntu 22.04 VM in VirtualBox
   # Disable network adapter
   # Install basic build tools (gcc, make)

   # Transfer package via shared folder
   # Run install script
   # Verify installation

--------------

Test Metrics
---------------

Coverage Metrics
~~~~~~~~~~~~~~~~

===================== ====== ===============
Metric                Target Measurement
===================== ====== ===============
**Line coverage**     80%+   cargo tarpaulin
**Branch coverage**   75%+   cargo tarpaulin
**Function coverage** 90%+   cargo tarpaulin
===================== ====== ===============

Quality Metrics
~~~~~~~~~~~~~~~

========================== ================ ================
Metric                     Target           Measurement
========================== ================ ================
**Clippy warnings**        0                cargo clippy
**Formatting issues**      0                cargo fmt –check
**Documentation coverage** 100% public APIs cargo doc
========================== ================ ================

Performance Metrics
~~~~~~~~~~~~~~~~~~~

========================= ======== =========
Metric                    Target   Test Case
========================= ======== =========
**Package prep time**     < 5 min  TC-110
**Large download memory** < 100 MB TC-111
**Install time**          < 20 min TC-113
========================= ======== =========

--------------

Test Schedule
----------------

Phase 1: Core Infrastructure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- TC-001 to TC-005 (Manifest parsing)
- Unit tests for core types

Phase 2: Built-in Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- TC-010 to TC-013 (RustApp)
- TC-020 to TC-023 (ExternalBinary)
- TC-030 to TC-035 (ModelFile)

Phase 3: Packaging
~~~~~~~~~~~~~~~~~~

- TC-040 to TC-044 (Packaging)

Phase 4: Install Scripts
~~~~~~~~~~~~~~~~~~~~~~~~

- TC-050 to TC-055 (Install scripts)

Phase 5: CLI
~~~~~~~~~~~~

- TC-060 to TC-066 (CLI interface)

Phase 6: Integration & System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- TC-070 to TC-073 (Error handling)
- TC-100 to TC-102 (End-to-end workflows)
- TC-110 to TC-113 (Performance)
- TC-120 to TC-123 (Security)

--------------

Defect Management
--------------------

Severity Levels
~~~~~~~~~~~~~~~

+---------------------+-------------------------------+-----------------------------+
| Severity            | Description                   | Example                     |
+=====================+===============================+=============================+
| **Critical**        | Blocks development/deployment | Package creation fails      |
+---------------------+-------------------------------+-----------------------------+
| **High**            | Major functionality broken    | Checksum verification fails |
+---------------------+-------------------------------+-----------------------------+
| **Medium**          | Feature impaired              | Progress bar doesn’t show   |
+---------------------+-------------------------------+-----------------------------+
| **Low**             | Minor issue                   | Typo in help text           |
+---------------------+-------------------------------+-----------------------------+

Defect Tracking
~~~~~~~~~~~~~~~

- Use GitHub Issues
- Label with severity (critical, high, medium, low)
- Tag with affected component
- Link to failing test case

--------------

Test Deliverables
--------------------

Test Code
~~~~~~~~~

- ``tests/`` directory with all test files
- ``tests/fixtures/`` with test manifests and data
- ``benches/`` with performance benchmarks

Test Reports
~~~~~~~~~~~~

- CI test results (GitHub Actions)
- Coverage reports (HTML from tarpaulin)
- Performance benchmark results

Test Documentation
~~~~~~~~~~~~~~~~~~

- This test plan
- Test case documentation (inline in test code)
- Testing guide for contributors

--------------

Risks and Mitigation
-----------------------

+-------------------------------+---------------------+---------------------------------------------+
| Risk                          | Impact              | Mitigation                                  |
+===============================+=====================+=============================================+
| Network-dependent tests flaky | High                | Mock network calls, use test fixtures       |
+-------------------------------+---------------------+---------------------------------------------+
| Platform-specific bugs        | Medium              | CI matrix with all platforms                |
+-------------------------------+---------------------+---------------------------------------------+
| Large file tests slow         | Medium              | Use smaller test files, separate slow tests |
+-------------------------------+---------------------+---------------------------------------------+
| Air-gapped VM setup complex   | Low                 | Document setup, provide VM image            |
+-------------------------------+---------------------+---------------------------------------------+

--------------

Approval
------------

Test plan will be approved when:

- ✅ All test cases defined
- ✅ CI/CD pipeline configured
- ✅ Test environment documented
- ✅ Coverage targets set
- ✅ Ready to begin testing during implementation

**Status:** ✅ Test Plan Complete - Ready for implementation

--------------

Requirements Traceability
-------------------------

This section demonstrates bidirectional traceability between requirements and test cases for AirGap Deploy.

Requirements to Tests Matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following table shows all requirements and their associated test cases. The "Incoming" column shows which tests validate each requirement.

.. needtable::
   :types: req, nfreq
   :columns: id, title, status, incoming
   :filter: "deploy" in tags
   :style: table

Requirements Coverage Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This table provides an overview of all AirGap Deploy requirements with their priority and status.

.. needtable::
   :types: req, nfreq
   :columns: id, title, priority, status
   :filter: "deploy" in tags
   :style: table

.. note::

   **Understanding Traceability:**

   - **Incoming links** show which test cases validate each requirement
   - **Tests column** (in test tables below) shows which requirements each test validates
   - This bidirectional linking ensures complete coverage and traceability

Test Cases
~~~~~~~~~~

This table lists all test cases with their validation links.

.. needtable::
   :types: test
   :columns: id, title, priority, status, tests
   :filter: "deploy" in tags
   :style: table

The "Tests" column shows which requirements each test case validates (via the :tests: link).

--------------

**End of Test Plan**
