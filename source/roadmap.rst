Project Roadmap
===============

Build a deployment tool that makes air-gap packaging simple. Ship it. See what happens.

**Guiding document:** :doc:`Principles </meta/principles>`

--------------

v1.0.0 Release
--------------

**Release Goal:** This project will reach v1.0.0 as part of a coordinated release with Cleanroom Whisper and AirGap Transfer.

**v1.0.0 Scope:** The MVP features documented in this roadmap.

**Cross-Project Integration:** v1.0.0 validates the Ollama deployment workflow works end-to-end.

**Release Coordination:** See :doc:`Release Roadmap </meta/release-roadmap>` for cross-project timeline and integration milestones.

**Target Date:** [TBD - see Release Roadmap]

--------------

Current Status
--------------

**Phase:** Planning Complete

**Next:** Begin MVP implementation

All requirements, design, and test specifications are complete. Ready to start Phase 1.

**MVP Goal:** Implement MVP that can package Cleanroom Whisper for air-gapped systems.

--------------

MVP Scope
---------

==================== =========================================
Feature              Implementation
==================== =========================================
Declarative Manifest Define requirements in AirGapDeploy.toml
RustApp Component    Vendor dependencies, include toolchain
External Binary      Clone repos, build instructions
Model Files          Download with checksums
Packaging            Create tar.gz/zip archives
Install Scripts      Generate platform-specific install.sh/ps1
CLI Interface        Prep, validate, init commands
==================== =========================================

--------------

Implementation Phases
---------------------

Phase 1: Core Infrastructure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Establish project structure and core abstractions

**Project Setup:**

- ☐ Create new cargo workspace with two crates
- ☐ Set up CI/CD (GitHub Actions)
- ☐ Configure cargo-deny for license compliance
- ☐ Add basic README, CONTRIBUTING.md, CODE_OF_CONDUCT.md

**Core Types** (src/core/):

- ☐ Platform - OS/architecture abstraction
- ☐ Target - Deployment target specification
- ☐ Component - Trait definition for all component types
- ☐ Manifest - AirGapDeploy.toml structure (using serde)
- ☐ Error - Unified error type (using thiserror)

**Manifest Parser** (src/manifest.rs):

- ☐ Define AirGapDeploy.toml schema
- ☐ Implement TOML parsing (using toml crate)
- ☐ Validation logic
- ☐ Schema versioning support

**Component Registry** (src/registry.rs):

- ☐ Component registration system
- ☐ Built-in component auto-registration
- ☐ Plugin discovery mechanism (optional)

**Done when:** Working manifest parser with validation, type-safe component registration, 80%+ test coverage for core types.

--------------

Phase 2: Built-in Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Implement the four essential component types

**RustAppComponent** (src/components/rust_app.rs):

- ☐ Source code collection
- ☐ cargo vendor integration
- ☐ Rust toolchain downloader (from static.rust-lang.org)
- ☐ Optional cross-compilation support (using cross)
- ☐ Generate .cargo/config.toml for vendored deps

**ExternalBinaryComponent** (src/components/external_binary.rs):

- ☐ Git repository cloning
- ☐ Tarball download support
- ☐ Build instruction templating
- ☐ Multi-platform binary support

**ModelFileComponent** (src/components/model_file.rs):

- ☐ HTTP download with progress bar (using reqwest + indicatif)
- ☐ Checksum verification (SHA256)
- ☐ Resume support for large files
- ☐ Multiple file sources (URL, local path)

**SystemPackageComponent** (src/components/system_package.rs):

- ☐ Linux distro detection (Debian, Fedora, Arch)
- ☐ Package download (apt, dnf, pacman)
- ☐ Dependency resolution (basic)
- ☐ Package metadata extraction

**Done when:** Four working component types, integration tests for each component, example manifests.

--------------

Phase 3: Collection & Packaging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Orchestrate components and create deployment packages

**Collector Engine** (src/collector.rs):

- ☐ Component execution orchestration
- ☐ Parallel collection (using rayon)
- ☐ Progress reporting
- ☐ Error handling and rollback
- ☐ Temporary directory management

**Packager** (src/packager.rs):

- ☐ Create tar.gz archives (Linux/macOS)
- ☐ Create zip archives (Windows)
- ☐ Package structure layout
- ☐ Metadata file generation (airgap-deploy-metadata.json)
- ☐ Compression level configuration

**Package Verification:**

- ☐ Checksum generation for package
- ☐ Content manifest (list of all files)
- ☐ Size validation

**Done when:** End-to-end package creation, package format documentation, benchmarks for collection/packaging performance.

--------------

Phase 4: Installation Script Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Generate platform-specific installation scripts

**Template System** (src/templates/):

- ☐ Tera template engine integration
- ☐ install.sh.tera - Bash script template
- ☐ install.ps1.tera - PowerShell script template
- ☐ README.txt.tera - Package documentation

**Install Step Compiler** (src/installer.rs):

- ☐ Convert InstallStep to shell commands
- ☐ Platform-specific command mapping
- ☐ Error handling in generated scripts
- ☐ Idempotency checks (detect existing installations)

**Script Features:**

- ☐ Dependency checking (Rust, git, make, etc.)
- ☐ Interactive prompts (install location)
- ☐ Progress output
- ☐ Logging to install.log
- ☐ Dry-run mode

**Done when:** Working install script generation, scripts tested on all target platforms, script documentation.

--------------

Phase 5: CLI Interface
~~~~~~~~~~~~~~~~~~~~~~

**Goal:** User-friendly command-line interface

**CLI Structure** (src/cli.rs, src/main.rs):

- ☐ Command parsing (using clap)
- ☐ airgap-deploy prep - Prepare deployment package
- ☐ airgap-deploy install - Install from package (optional)
- ☐ airgap-deploy validate - Validate manifest
- ☐ airgap-deploy list-components - Show available components
- ☐ airgap-deploy init - Create template AirGapDeploy.toml

**User Experience:**

- ☐ Colored output (using colored crate)
- ☐ Progress bars (using indicatif)
- ☐ Spinner for long operations
- ☐ Clear error messages with suggestions
- ☐ --verbose flag for debugging

**Configuration:**

- ☐ Global config file (~/.airgap-deploy/config.toml)
- ☐ Default target platform
- ☐ Cache directory for downloads
- ☐ Proxy settings

**Done when:** Polished CLI experience, help documentation (--help), man page generation.

--------------

Phase 6: Testing & Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Comprehensive testing and documentation

**Unit Tests:**

- ☐ Core types (platform, target, component trait)
- ☐ Manifest parsing (valid/invalid cases)
- ☐ Component logic (each built-in component)
- ☐ Template rendering

**Integration Tests:**

- ☐ End-to-end: manifest → package → install
- ☐ Multi-platform testing (Linux, macOS, Windows via CI)
- ☐ Error scenarios (missing dependencies, network failures)
- ☐ Large package handling (multi-GB models)

**Documentation:**

- ☐ API documentation (rustdoc)
- ☐ User guide (docs/guide.md) - Getting started, manifest reference, component types, best practices
- ☐ Developer guide (docs/developers.md) - Architecture, custom components, contributing
- ☐ Examples - Rust application, Python application, ML application with models

**CI/CD:**

- ☐ Run tests on Linux, macOS, Windows
- ☐ Clippy lints (deny warnings)
- ☐ rustfmt checks
- ☐ cargo-deny license checks
- ☐ Release automation (GitHub releases)

**Done when:** 80%+ code coverage, complete documentation, working examples, CI/CD pipeline.

--------------

Phase 7: Plugin System (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Support custom component plugins

**Plugin Discovery:**

- ☐ Load plugins from airgap-components/ directory
- ☐ Dynamic library loading (using libloading)
- ☐ Plugin API versioning
- ☐ Plugin safety checks

**Plugin Development Kit:**

- ☐ airgap-plugin crate with Component trait
- ☐ Plugin template generator (airgap plugin new)
- ☐ Plugin testing utilities
- ☐ Plugin packaging (cdylib)

**Examples:**

- ☐ TensorFlow model plugin
- ☐ Docker container plugin
- ☐ Database dump plugin

**Done when:** Working plugin system, plugin development guide, example plugins.

--------------

Definition of Done
------------------

MVP is complete when:

☐ Successfully packages Cleanroom Whisper for all platforms
☐ Generated install scripts work on air-gapped VMs
☐ Package creation completes efficiently for typical applications
☐ 80%+ code coverage
☐ Zero clippy warnings
☐ All licenses compatible with MIT/Apache-2.0
☐ First-time user can create package quickly and easily
☐ Documentation covers all use cases

--------------

What's NOT in MVP
-----------------

Defer all of this until after shipping:

- GUI interface (CLI only)
- Network-based distribution (local packaging only)
- Digital signatures/verification (future enhancement)
- Automatic updates (contradicts air-gap philosophy)
- SystemPackageComponent (defer to v0.2)
- Plugin system (Phase 7 - defer to v0.2+)
- Tests (partial - basic tests only)
- Comprehensive documentation (minimal docs for MVP)

Build it. Use it. Then improve it.

--------------

After MVP
---------

**v0.2 - Enhanced Components:**
- PythonAppComponent (pip, virtualenv)
- NodeAppComponent (npm, package-lock.json)
- GoAppComponent (go mod vendor)

**v1.0 - Advanced Features:**
- Delta updates (only changed files)
- Multi-platform single package
- Binary patching for updates

**v1.1 - Enterprise Features:**
- Digital signatures (GPG, Sigstore)
- SBOM generation (Software Bill of Materials)
- Compliance reporting
- License scanning

**v2.0 - Major Evolution:**
- Full plugin system
- GUI (Tauri-based)
- Package repository format
- Incremental syncing

--------------

Key Documents
-------------

============================================== =======================================
Document                                       Purpose
============================================== =======================================
:doc:`Principles </meta/principles>`           Design principles (read first)
:doc:`Requirements (SRS) <requirements/srs>`   Functional and non-functional requirements
:doc:`Design (SDD) <design/sdd>`               Architecture and component design
:doc:`Test Plan <testing/plan>`                Test cases with traceability
============================================== =======================================

--------------

See Also
--------

- :doc:`Meta-Architecture </meta/meta-architecture>` - How airgap-deploy fits in the AirGap suite
- :doc:`Requirements Overview </meta/requirements-overview>` - Project statistics and requirements overview
- :doc:`Cleanroom Whisper </airgap-whisper/readme>` - Primary use case
- :doc:`AirGap Transfer </airgap-transfer/readme>` - Large file transfer companion tool

--------------

Progress Log
------------

========== =======================================
Date       Activity
========== =======================================
2026-01-04 Created specification and documentation
========== =======================================
