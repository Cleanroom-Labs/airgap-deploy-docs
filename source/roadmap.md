# Project Roadmap

Build a deployment tool that makes air-gap packaging simple. Ship it. See what happens.

<br>

**Guiding document:** [Principles](https://cleanroomlabs.dev/docs/meta/principles.html)

## v1.0.0 Release

**Release Goal:** This project will reach v1.0.0 as part of a coordinated release with Cleanroom Whisper and AirGap Transfer.

**v1.0.0 Scope:** The MVP features documented in this roadmap.

**Cross-Project Integration:** v1.0.0 validates the Ollama deployment workflow works end-to-end.

**Release Coordination:** See [Release Roadmap](https://cleanroomlabs.dev/docs/meta/release-roadmap.html) for cross-project timeline and integration milestones.

<br>

**Target:** Suite Milestone 3 (Month 6) — MVP Complete

**Note:** Development begins at project start (Suite Milestone 1) and continues through Suite Milestone 3.

## Current Status

**Phase:** Preliminary Planning Complete

**Next:** Finalize plan and begin MVP implementation

Requirements, design, and test specifications need some minor adjustments and a final review.

<br>

**MVP Goal:** Implement MVP that can package Cleanroom Whisper for air-gapped systems.

## MVP Scope

| Feature | Implementation |
|---------|----------------|
| Declarative Manifest | Define requirements in AirGapDeploy.toml |
| RustApp Component | Vendor dependencies, include toolchain |
| External Binary | Clone repos, build instructions |
| Model Files | Download with checksums |
| Packaging | Create tar.gz/zip archives |
| Install Scripts | Generate platform-specific install.sh/ps1 |
| CLI Interface | Prep, validate, init commands |

## Implementation Phases

### Phase 1: Core Infrastructure

**Target:** Suite Milestone 1 (Month 2)

**Goal:** Establish project structure and core abstractions

**Project Setup:**

- [ ] Create new cargo workspace with two crates
- [ ] Set up CI/CD (GitHub Actions)
- [ ] Configure cargo-deny for license compliance
- [ ] Add basic README, CONTRIBUTING.md, CODE_OF_CONDUCT.md

**Core Types** (src/core/):

- [ ] Platform - OS/architecture abstraction
- [ ] Target - Deployment target specification
- [ ] Component - Trait definition for all component types
- [ ] Manifest - AirGapDeploy.toml structure (using serde)
- [ ] Error - Unified error type (using thiserror)

**Manifest Parser** (src/manifest.rs):

- [ ] Define AirGapDeploy.toml schema
- [ ] Implement TOML parsing (using toml crate)
- [ ] Validation logic
- [ ] Schema versioning support

**Error Handling** (src/error.rs):

- [ ] Unified error type with context (using thiserror)
- [ ] Actionable error messages with recovery suggestions
- [ ] Non-zero exit codes for all failure modes
- [ ] Operation logging for debugging

**Component Registry** (src/registry.rs):

- [ ] Component registration system
- [ ] Built-in component auto-registration
- [ ] Plugin discovery mechanism (optional)

**Done when:** Working manifest parser with validation, type-safe component registration, error handling with recovery suggestions, 80%+ test coverage for core types.

### Phase 2: Built-in Components

**Target:** Suite Milestone 2 (Month 4)

**Goal:** Implement the four essential component types

**RustAppComponent** (src/components/rust_app.rs):

- [ ] Source code collection
- [ ] cargo vendor integration
- [ ] Rust toolchain downloader (from static.rust-lang.org)
- [ ] Optional cross-compilation support (using cross)
- [ ] Generate .cargo/config.toml for vendored deps

**ExternalBinaryComponent** (src/components/external_binary.rs):

- [ ] Git repository cloning
- [ ] Tarball download support
- [ ] Build instruction templating
- [ ] Multi-platform binary support

**ModelFileComponent** (src/components/model_file.rs):

- [ ] HTTP download with progress bar (using reqwest + indicatif)
- [ ] Checksum verification (SHA256)
- [ ] Resume support for large files
- [ ] Multiple file sources (URL, local path)

**SystemPackageComponent** (src/components/system_package.rs):

- [ ] Linux distro detection (Debian, Fedora, Arch)
- [ ] Package download (apt, dnf, pacman)
- [ ] Dependency resolution (basic)
- [ ] Package metadata extraction

**Done when:** Four working component types, integration tests for each component, example manifests.

### Phase 3: Collection & Packaging

**Target:** Suite Milestone 2–3

**Goal:** Orchestrate components and create deployment packages

**Collector Engine** (src/collector.rs):

- [ ] Component execution orchestration
- [ ] Parallel collection (using rayon)
- [ ] Progress reporting
- [ ] Error handling and rollback
- [ ] Temporary directory management

**Packager** (src/packager.rs):

- [ ] Create tar.gz archives (Linux/macOS)
- [ ] Create zip archives (Windows)
- [ ] Package structure layout
- [ ] Metadata file generation (airgap-deploy-metadata.json)
- [ ] Compression level configuration

**Package Verification:**

- [ ] Checksum generation for package
- [ ] Content manifest (list of all files)
- [ ] Size validation

**Done when:** End-to-end package creation, package format documentation, benchmarks for collection/packaging performance.

### Phase 4: Installation Script Generation

**Target:** Suite Milestone 3

**Goal:** Generate platform-specific installation scripts

**Template System** (src/templates/):

- [ ] Tera template engine integration
- [ ] install.sh.tera - Bash script template
- [ ] install.ps1.tera - PowerShell script template
- [ ] README.txt.tera - Package documentation

**Install Step Compiler** (src/installer.rs):

- [ ] Convert InstallStep to shell commands
- [ ] Platform-specific command mapping
- [ ] Error handling in generated scripts
- [ ] Idempotency checks (detect existing installations)

**Script Features:**

- [ ] Dependency checking (Rust, git, make, etc.)
- [ ] Interactive prompts (install location)
- [ ] Progress output
- [ ] Logging to install.log
- [ ] Dry-run mode

**Enhanced Installation Features:**

- [ ] Optional component declaration (`required` field)
- [ ] Component selection at prep time (`--include` flag)
- [ ] Config file generation from templates (`[install.config]`)
- [ ] Custom installation steps (`[install.steps]`)
- [ ] Interactive and automatic installation modes (`MODE=automatic`)
- [ ] Dependency declaration (`[install.dependencies]`)
- [ ] Disk space verification before installation

**Done when:** Working install script generation with component selection and config generation, scripts tested on all target platforms, script documentation.

### Phase 5: CLI Interface

**Target:** Suite Milestone 3

**Goal:** User-friendly command-line interface

**CLI Structure** (src/cli.rs, src/main.rs):

- [ ] Command parsing (using clap)
- [ ] airgap-deploy prep - Prepare deployment package
- [ ] airgap-deploy install - Install from package (optional)
- [ ] airgap-deploy validate - Validate manifest
- [ ] airgap-deploy list-components - Show available components
- [ ] airgap-deploy init - Create template AirGapDeploy.toml

**User Experience:**

- [ ] Colored output (using colored crate)
- [ ] Progress bars (using indicatif)
- [ ] Spinner for long operations
- [ ] Clear error messages with suggestions
- [ ] --verbose flag for debugging

**Configuration:**

- [ ] Global config file (~/.airgap-deploy/config.toml)
- [ ] Default target platform
- [ ] Cache directory for downloads
- [ ] Proxy settings

**Done when:** Polished CLI experience, help documentation (--help), man page generation.

### Phase 6: Testing & Documentation

**Target:** Suite Milestone 3 (Month 6) — MVP Complete

**Goal:** Comprehensive testing and documentation

**Unit Tests:**

- [ ] Core types (platform, target, component trait)
- [ ] Manifest parsing (valid/invalid cases)
- [ ] Component logic (each built-in component)
- [ ] Template rendering

**Integration Tests:**

- [ ] End-to-end: manifest → package → install
- [ ] Multi-platform testing (Linux, macOS, Windows via CI)
- [ ] Error scenarios (missing dependencies, network failures)
- [ ] Large package handling (multi-GB models)

**Documentation:**

- [ ] API documentation (rustdoc)
- [ ] User guide (docs/guide.md) - Getting started, manifest reference, component types, best practices
- [ ] Developer guide (docs/developers.md) - Architecture, custom components, contributing
- [ ] Examples - Rust application, Python application, ML application with models

**CI/CD:**

- [ ] Run tests on Linux, macOS, Windows
- [ ] Clippy lints (deny warnings)
- [ ] rustfmt checks
- [ ] cargo-deny license checks
- [ ] Release automation (GitHub releases)

**Done when:** 80%+ code coverage, complete documentation, working examples, CI/CD pipeline.

### Phase 7: Plugin System (Deferred to v1.1+)

**Target Date:** Deferred - not included in v1.0.0 release

**Goal:** Support custom component plugins

**Plugin Discovery:**

- [ ] Load plugins from airgap-components/ directory
- [ ] Dynamic library loading (using libloading)
- [ ] Plugin API versioning
- [ ] Plugin safety checks

**Plugin Development Kit:**

- [ ] airgap-plugin crate with Component trait
- [ ] Plugin template generator (airgap plugin new)
- [ ] Plugin testing utilities
- [ ] Plugin packaging (cdylib)

**Examples:**

- [ ] TensorFlow model plugin
- [ ] Docker container plugin
- [ ] Database dump plugin

**Done when:** Working plugin system, plugin development guide, example plugins.

## Definition of Done

MVP is complete when:

- [ ] Successfully packages Cleanroom Whisper for all platforms
- [ ] Generated install scripts work on air-gapped VMs
- [ ] Package creation completes efficiently for typical applications
- [ ] 80%+ code coverage
- [ ] Zero clippy warnings
- [ ] All dependency licenses compatible with AGPL-3.0
- [ ] First-time user can create package quickly and easily
- [ ] Documentation covers all use cases

## What's NOT in MVP

Defer all of this until after shipping:

- GUI interface (CLI only)
- Network-based distribution (local packaging only)
- Digital signatures/verification (future enhancement)
- Automatic updates (contradicts air-gap philosophy)

## After MVP

**Enhanced Components:**
- PythonAppComponent (pip, virtualenv)
- NodeAppComponent (npm, package-lock.json)
- GoAppComponent (go mod vendor)

**Enterprise Features:**
- Digital signatures (GPG, Sigstore)
- SBOM generation (Software Bill of Materials)
- Compliance reporting
- License scanning

## Key Documents

| Document | Purpose |
|----------|---------|
| [Principles](https://cleanroomlabs.dev/docs/meta/principles.html) | Design principles (read first) |
| [Requirements (SRS)](requirements/srs) | Functional and non-functional requirements |
| [Design (SDD)](design/sdd) | Architecture and component design |
| [Test Plan](testing/plan) | Test cases with traceability |

## See Also

- [Meta-Architecture](https://cleanroomlabs.dev/docs/meta/meta-architecture.html) - How AirGap Deploy fits in the AirGap suite
- [Specification Overview](https://cleanroomlabs.dev/docs/meta/specification-overview.html) - Project statistics and traceability overview
- [Cleanroom Whisper](https://cleanroomlabs.dev/docs/whisper/readme.html) - Primary use case
- [AirGap Transfer](https://cleanroomlabs.dev/docs/transfer/readme.html) - Large file transfer companion tool

## Progress Log

| Date | Activity |
|------|----------|
| 2026-01-28 | Created specification and documentation |
| 2026-01-31 | Updated roadmap to align with 6-milestone release plan |
