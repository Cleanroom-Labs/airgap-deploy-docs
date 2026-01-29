Software Design Document
========================

Introduction
------------

Purpose
~~~~~~~

This Software Design Document (SDD) describes the architectural and detailed design of **AirGap Deploy**, a command-line tool for packaging applications for air-gapped deployment.

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

This document is intended for:

- Developers implementing AirGap Deploy
- Code reviewers
- Future maintainers
- Contributors developing custom components

Scope
~~~~~

This document covers:

- System architecture and component decomposition
- Data structures and algorithms
- Interface specifications
- Design decisions and rationales

This document does NOT cover:

- Requirements (see :doc:`SRS <../requirements/srs>`)
- Implementation details (see source code)
- User documentation (see README)

System Architecture
-------------------

Architectural Style
~~~~~~~~~~~~~~~~~~~

AirGap Deploy follows a **pipeline architecture** with distinct stages:

::

   Input (Manifest) → Parse → Collect → Package → Generate Scripts → Output (Archive)

This architecture provides:

- **Clear separation of concerns:** Each stage has a single responsibility
- **Testability:** Each stage can be tested independently
- **Extensibility:** New component types can be added without modifying core pipeline

High-Level Architecture
~~~~~~~~~~~~~~~~~~~~~~~

::

   ┌──────────────────────────────────────────────────────────────────┐
   │                      airgap-deploy CLI                           │
   │                         (main.rs)                                │
   └────────────────────────────┬─────────────────────────────────────┘
                                │
                   ┌────────────┴────────────┐
                   │      CLI Parser         │
                   │      (clap)             │
                   └────────────┬────────────┘
                                │
               ┌────────────────┴────────────────┐
               │                                 │
       ┌───────▼────────┐              ┌────────▼────────┐
       │  prep command  │              │ validate, init  │
       │                │              │ list-components │
       └───────┬────────┘              └─────────────────┘
               │
               ├─────────────────────────────────────────┐
               │                                         │
       ┌───────▼────────┐                       ┌────────▼────────┐
       │ Manifest Parser│                       │   Collector     │
       │  (manifest.rs) │                       │ (collector.rs)  │
       └───────┬────────┘                       └────────┬────────┘
               │                                         │
               │ produces                                │ uses
               │                                         │
       ┌───────▼────────┐                       ┌────────▼────────┐
       │   Manifest     │                       │ Component       │
       │   (struct)     │                       │ Registry        │
       └────────────────┘                       │ (registry.rs)   │
                                                └────────┬────────┘
                                                         │
                                            ┌────────────┴─────────────┐
                                            │                          │
                                   ┌────────▼────────┐       ┌─────────▼────────┐
                                   │  RustApp        │       │ ExternalBinary   │
                                   │  Component      │       │ Component        │
                                   └─────────────────┘       └──────────────────┘
                                   ┌─────────────────┐       ┌──────────────────┐
                                   │  ModelFile      │       │ SystemPackage    │
                                   │  Component      │       │ Component        │
                                   └─────────────────┘       └──────────────────┘
                                            │
                                            │ collected files
                                            │
                                   ┌────────▼────────┐
                                   │   Packager      │
                                   │ (packager.rs)   │
                                   └────────┬────────┘
                                            │
                                            ├─────────────────┐
                                            │                 │
                                   ┌────────▼────────┐  ┌─────▼───────────┐
                                   │ Install Script  │  │ Package Archive │
                                   │ Generator       │  │ (.tar.gz/.zip)  │
                                   │ (installer.rs)  │  │                 │
                                   └─────────────────┘  └─────────────────┘

Component Descriptions
~~~~~~~~~~~~~~~~~~~~~~

+------------------------------+------------------------------------------+------------------------------------------------------+
| Component                    | Responsibility                           | Key Types                                            |
+==============================+==========================================+======================================================+
| **CLI Parser**               | Parse command-line arguments             | ``Cli``, ``PrepCommand``, ``ValidateCommand``        |
+------------------------------+------------------------------------------+------------------------------------------------------+
| **Manifest Parser**          | Parse and validate TOML manifests        | ``Manifest``, ``PackageConfig``, ``ComponentConfig`` |
+------------------------------+------------------------------------------+------------------------------------------------------+
| **Component Registry**       | Register and instantiate component types | ``ComponentRegistry``, ``Component`` trait           |
+------------------------------+------------------------------------------+------------------------------------------------------+
| **Collector**                | Orchestrate component collection         | ``Collector``, ``CollectionResult``                  |
+------------------------------+------------------------------------------+------------------------------------------------------+
| **Built-in Components**      | Implement specific component types       | ``RustAppComponent``, ``ModelFileComponent``, etc.   |
+------------------------------+------------------------------------------+------------------------------------------------------+
| **Packager**                 | Create deployment archives               | ``Packager``, ``PackageLayout``                      |
+------------------------------+------------------------------------------+------------------------------------------------------+
| **Install Script Generator** | Generate installation scripts            | ``InstallGenerator``, ``InstallStep``                |
+------------------------------+------------------------------------------+------------------------------------------------------+

Detailed Design
---------------

Core Data Structures
~~~~~~~~~~~~~~~~~~~~

Manifest Structure
^^^^^^^^^^^^^^^^^^

.. code:: rust

   /// Top-level manifest structure
   pub struct Manifest {
       pub package: PackageConfig,
       pub targets: Option<TargetsConfig>,
       pub components: Vec<ComponentConfig>,
       pub install: Option<InstallConfig>,
   }

   /// Package metadata
   pub struct PackageConfig {
       pub name: String,
       pub version: String,
       pub description: String,
   }

   /// Target platforms configuration
   pub struct TargetsConfig {
       pub platforms: Vec<Platform>,
       pub default: Platform,
   }

   /// Platform identification
   pub enum Platform {
       LinuxX86_64,
       LinuxAarch64,
       MacOSX86_64,
       MacOSAarch64,
       WindowsX86_64,
   }

   /// Component configuration (polymorphic)
   pub struct ComponentConfig {
       pub component_type: String,  // "rust-app", "external-binary", etc.
       pub config: serde_json::Value,  // Component-specific config
   }

   /// Installation configuration
   pub struct InstallConfig {
       pub method: InstallMethod,
       pub install_to: InstallLocation,
       pub mode: InstallMode,
       pub config: Option<ConfigTemplate>,
       pub steps: Option<HashMap<String, Vec<String>>>,
   }

   pub enum InstallMethod {
       BuildFromSource,
       PrebuiltBinary,
   }

   pub enum InstallLocation {
       User,    // ~/.local or %LOCALAPPDATA%
       System,  // /usr/local or C:\Program Files
   }

   pub enum InstallMode {
       Interactive,
       Automatic,
   }

Component Trait
^^^^^^^^^^^^^^^

.. code:: rust

   /// Trait that all components must implement
   pub trait Component: Send + Sync {
       /// Collect this component's files to the staging directory
       fn collect(&self, staging_dir: &Path, context: &CollectionContext) -> Result<CollectionResult>;

       /// Get the component's name
       fn name(&self) -> &str;

       /// Get installation steps for this component
       fn install_steps(&self) -> Vec<InstallStep>;

       /// Validate component configuration
       fn validate(&self) -> Result<()>;
   }

   /// Context provided during collection
   pub struct CollectionContext {
       pub target_platform: Platform,
       pub cache_dir: PathBuf,
       pub progress: ProgressBar,
   }

   /// Result of component collection
   pub struct CollectionResult {
       pub collected_files: Vec<CollectedFile>,
       pub metadata: ComponentMetadata,
   }

   pub struct CollectedFile {
       pub source_path: PathBuf,
       pub relative_path: PathBuf,  // Path within package
       pub checksum: Option<String>,
   }

Install Steps
^^^^^^^^^^^^^

.. code:: rust

   /// Installation step for generated scripts
   pub enum InstallStep {
       CheckDependency {
           name: String,
           command: String,  // e.g., "rustc --version"
           install_if_missing: bool,
       },
       ExecuteCommand {
           command: String,
           working_dir: Option<PathBuf>,
           description: String,
       },
       CopyFile {
           source: PathBuf,
           destination: PathBuf,
           permissions: Option<u32>,
       },
       GenerateConfig {
           template: String,
           output_path: PathBuf,
           variables: HashMap<String, String>,
       },
       CreateDirectory {
           path: PathBuf,
           permissions: Option<u32>,
       },
   }

Component Implementations
~~~~~~~~~~~~~~~~~~~~~~~~~

RustAppComponent
^^^^^^^^^^^^^^^^

**Purpose:** Package Rust applications with vendored dependencies

**Configuration:**

.. code:: toml

   [[components]]
   type = "rust-app"
   source = "."
   vendor = true
   include_toolchain = true
   prebuild = false

**Collection Algorithm:**

Locate Cargo.toml in source directory
If ``vendor = true``:

   - Execute ``cargo vendor`` to download dependencies
   - Create ``.cargo/config.toml`` with vendored paths

If ``include_toolchain = true``:

   - Download Rust toolchain installer from static.rust-lang.org
   - Include in ``rust-installer/`` directory

Copy source code and vendor directory to staging
If ``prebuild = true``:

   - Execute ``cargo build --release``
   - Include prebuilt binary (deferred to v0.2)

**Install Steps:**

.. code:: rust

   vec![
       InstallStep::CheckDependency {
           name: "Rust".to_string(),
           command: "rustc --version".to_string(),
           install_if_missing: true,  // Use included installer
       },
       InstallStep::ExecuteCommand {
           command: "cargo build --release --offline".to_string(),
           working_dir: Some(PathBuf::from("app-source")),
           description: "Building Rust application".to_string(),
       },
       InstallStep::CopyFile {
           source: PathBuf::from("app-source/target/release/app-name"),
           destination: PathBuf::from("{{ install_prefix }}/bin/app-name"),
           permissions: Some(0o755),
       },
   ]

ExternalBinaryComponent
^^^^^^^^^^^^^^^^^^^^^^^

**Purpose:** Include external binaries that need to be built from source

**Configuration:**

.. code:: toml

   [[components]]
   type = "external-binary"
   name = "whisper.cpp"
   repo = "https://github.com/ggerganov/whisper.cpp.git"
   tag = "v1.0.0"
   build_instructions = "make"

**Collection Algorithm:** 1. Clone Git repository to staging directory 2. Checkout specified branch/tag/commit 3. Include entire repository (for offline build) 4. Store build instructions for install script

**Install Steps:**

.. code:: rust

   vec![
       InstallStep::CheckDependency {
           name: "C compiler".to_string(),
           command: "gcc --version || clang --version".to_string(),
           install_if_missing: false,
       },
       InstallStep::ExecuteCommand {
           command: "make".to_string(),  // From build_instructions
           working_dir: Some(PathBuf::from("whisper.cpp")),
           description: "Building whisper.cpp".to_string(),
       },
       InstallStep::CopyFile {
           source: PathBuf::from("whisper.cpp/main"),
           destination: PathBuf::from("{{ install_prefix }}/bin/whisper-main"),
           permissions: Some(0o755),
       },
   ]

ModelFileComponent
^^^^^^^^^^^^^^^^^^

**Purpose:** Download large model files with checksum verification

**Configuration:**

.. code:: toml

   [[components]]
   type = "model-file"
   name = "base.en"
   url = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin"
   checksum = "sha256:abc123..."
   required = true
   install_path = "models/base.en.bin"

**Collection Algorithm:**

Check cache directory for existing file with matching checksum
If not cached:

   - Download file from URL with progress bar
   - Support resume via HTTP Range requests
   - Stream to disk (don't load entire file in memory)

Verify SHA-256 checksum
Copy to staging directory

**Install Steps:**

.. code:: rust

   vec![
       InstallStep::CreateDirectory {
           path: PathBuf::from("{{ install_prefix }}/share/app-name/models"),
           permissions: Some(0o755),
       },
       InstallStep::CopyFile {
           source: PathBuf::from("models/base.en.bin"),
           destination: PathBuf::from("{{ install_prefix }}/share/app-name/models/base.en.bin"),
           permissions: Some(0o644),
       },
   ]

Packaging Algorithm
~~~~~~~~~~~~~~~~~~~

**Input:** Staging directory with collected components **Output:** Compressed archive (.tar.gz or .zip)

**Algorithm:**

::

   1. Create package layout in staging directory:
      - install.sh / install.ps1 (generated)
      - README.txt (generated)
      - airgap-deploy-metadata.json (generated)
      - Component files (already collected)

   2. Generate install scripts:
      a. Render Tera templates with component install steps
      b. Include dependency checking logic
      c. Include error handling and logging
      d. Include interactive/automatic mode support

   3. Generate README.txt:
      - Package name, version, description
      - Installation instructions
      - Component list
      - System requirements

   4. Generate metadata JSON:
      {
        "package_name": "...",
        "version": "...",
        "target_platform": "...",
        "components": [...],
        "created_at": "...",
        "airgap_deploy_version": "..."
      }

   5. Create archive:
      - Linux/macOS: tar czf package.tar.gz package-dir/
      - Windows: Zip package.zip package-dir/

   6. Generate package checksum:
      - SHA-256 of final archive
      - Save to package.tar.gz.sha256

Install Script Template
~~~~~~~~~~~~~~~~~~~~~~~

**Bash Template (install.sh.tera):**

.. code:: bash

   #!/bin/bash
   set -e

   # Generated by airgap-deploy {{ airgap_deploy_version }}
   # Package: {{ package_name }} v{{ package_version }}
   # Target: {{ target_platform }}

   INSTALL_PREFIX="${INSTALL_PREFIX:-$HOME/.local}"
   MODE="${MODE:-interactive}"
   LOG_FILE="install.log"

   echo "=== {{ package_name }} Installation ===" | tee -a "$LOG_FILE"
   echo "Target: {{ target_platform }}" | tee -a "$LOG_FILE"
   echo "" | tee -a "$LOG_FILE"

   # Dependency checking
   {% for dep in dependencies %}
   if ! command -v {{ dep.command }} &> /dev/null; then
       {% if dep.install_if_missing %}
       echo "Installing {{ dep.name }}..." | tee -a "$LOG_FILE"
       # Install logic here
       {% else %}
       echo "ERROR: {{ dep.name }} not found. Please install it first." | tee -a "$LOG_FILE"
       exit 1
       {% endif %}
   fi
   {% endfor %}

   # Interactive mode: prompt for install location
   if [ "$MODE" = "interactive" ]; then
       read -p "Installation directory [$INSTALL_PREFIX]: " USER_PREFIX
       INSTALL_PREFIX="${USER_PREFIX:-$INSTALL_PREFIX}"
   fi

   echo "Installing to: $INSTALL_PREFIX" | tee -a "$LOG_FILE"

   # Execute install steps
   {% for step in install_steps %}
   echo "{{ step.description }}" | tee -a "$LOG_FILE"
   {{ step.command }} 2>&1 | tee -a "$LOG_FILE"
   {% endfor %}

   echo "" | tee -a "$LOG_FILE"
   echo "Installation complete!" | tee -a "$LOG_FILE"
   echo "Installed to: $INSTALL_PREFIX" | tee -a "$LOG_FILE"

Interface Specifications
------------------------

Component Plugin Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Future Enhancement:** Plugin system for custom component types

.. code:: rust

   // Plugin trait (future)
   pub trait ComponentPlugin {
       fn name(&self) -> &str;
       fn version(&self) -> &str;
       fn create_component(&self, config: serde_json::Value) -> Result<Box<dyn Component>>;
   }

   // Plugin discovery (future)
   pub struct PluginLoader {
       plugin_dir: PathBuf,
   }

   impl PluginLoader {
       pub fn load_plugins(&self) -> Result<Vec<Box<dyn ComponentPlugin>>> {
           // Load dynamic libraries from plugin_dir
           // Instantiate plugins
           // Validate API version compatibility
       }
   }

**Note:** Plugin system deferred to post-v1.0 (see :doc:`Roadmap <../roadmap>` Phase 7)

Design Decisions and Rationales
-------------------------------

Why TOML for Manifests?
~~~~~~~~~~~~~~~~~~~~~~~

**Decision:** Use TOML format for ``AirGapDeploy.toml``

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Alternatives Considered:**

- YAML: Too flexible, whitespace-sensitive
- JSON: Not human-friendly for configuration
- Custom DSL: Too much complexity

**Rationale:**

- TOML is human-readable and writable
- Strongly typed (better validation)
- Good Rust ecosystem support (serde, toml crate)
- Used by Cargo.toml (familiar to Rust developers)

Why Build from Source on Air-Gapped System?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Decision:** Build applications on air-gapped system rather than prebuilding

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Alternatives Considered:**

- Prebuild binaries for all platforms
- Cross-compilation on developer machine

**Rationale:**

- **Trust:** User can inspect source before building
- **Flexibility:** Supports different system configurations (ALSA, GPU, etc.)
- **Simplicity:** No cross-compilation toolchain setup required
- **MVP Scope:** Prebuilding can be added later as optional optimization

**Trade-off:** Requires build tools on air-gapped system, longer installation time

Why Component Trait Instead of Enums?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Decision:** Use trait-based design for components

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Alternatives Considered:**

- Enum with variants for each component type
- Struct with function pointers

**Rationale:**

- **Extensibility:** Easy to add new component types without modifying core
- **Plugin System:** Enables future plugin architecture
- **Separation of Concerns:** Each component type is independent module
- **Testing:** Can mock components for unit tests

**Trade-off:** Slightly more complex than enum, uses dynamic dispatch

Why Generate Install Scripts Instead of Installing Directly?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Decision:** Generate standalone installation scripts

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Alternatives Considered:**

- ``airgap-deploy install`` command that must run on air-gapped system
- Require AirGap Deploy binary on both sides

**Rationale:**

- **Self-contained:** Package includes everything needed, no external dependencies
- **Inspectable:** User can review install script before running
- **Platform-native:** Bash/PowerShell are standard on target systems
- **Flexibility:** User can customize script if needed

**Trade-off:** Less control over installation process, script generation complexity

Error Handling Strategy
-----------------------

Error Types
~~~~~~~~~~~

.. code:: rust

   #[derive(Debug, thiserror::Error)]
   pub enum Error {
       #[error("Manifest parse error: {0}")]
       ManifestParse(#[from] toml::de::Error),

       #[error("Component collection failed: {0}")]
       ComponentCollection(String),

       #[error("Network error: {0}")]
       Network(#[from] reqwest::Error),

       #[error("IO error: {0}")]
       Io(#[from] std::io::Error),

       #[error("Checksum mismatch for {file}: expected {expected}, got {actual}")]
       ChecksumMismatch {
           file: String,
           expected: String,
           actual: String,
       },

       #[error("Component not found: {0}")]
       ComponentNotFound(String),
   }

Error Recovery
~~~~~~~~~~~~~~

**Network Errors:**

- Retry up to 3 times with exponential backoff
- Display clear message with retry attempt number
- Suggest checking network connection

**Checksum Errors:**

- Display expected vs actual checksum
- Suggest re-downloading file or updating manifest
- Do NOT proceed with mismatched checksums

**IO Errors:**

- Display file path and operation that failed
- Suggest checking disk space and permissions
- Clean up temporary files on failure

Logging
~~~~~~~

**Levels:**

- ERROR: Critical failures that prevent completion
- WARN: Non-fatal issues that might affect operation
- INFO: Normal operational messages (default)
- DEBUG: Detailed information for troubleshooting (–verbose)
- TRACE: Very detailed, internal state information

**Output:**

- Console: INFO and above (with colors)
- Log file (optional): DEBUG and above

Performance Considerations
--------------------------

Parallel Collection
~~~~~~~~~~~~~~~~~~~

**Optimization:** Collect components in parallel using rayon

.. code:: rust

   use rayon::prelude::*;

   pub fn collect_all_components(
       components: Vec<Box<dyn Component>>,
       staging_dir: &Path,
       context: &CollectionContext,
   ) -> Result<Vec<CollectionResult>> {
       components
           .par_iter()  // Parallel iterator
           .map(|component| component.collect(staging_dir, context))
           .collect::<Result<Vec<_>>>()
   }

**Benefit:** Reduces total collection time by 50-70% for manifests with multiple independent components

Streaming Downloads
~~~~~~~~~~~~~~~~~~~

**Optimization:** Stream large files to disk, don’t load in memory

.. code:: rust

   pub fn download_file(url: &str, dest: &Path) -> Result<()> {
       let mut response = reqwest::blocking::get(url)?;
       let mut file = File::create(dest)?;

       // Stream in chunks
       std::io::copy(&mut response, &mut file)?;

       Ok(())
   }

**Benefit:** Constant memory usage regardless of file size (can handle 50GB+ files)

Caching
~~~~~~~

**Optimization:** Cache downloaded files by checksum

.. code:: rust

   pub fn get_cached_file(url: &str, checksum: &str, cache_dir: &Path) -> Option<PathBuf> {
       let cache_path = cache_dir.join(checksum);
       if cache_path.exists() && verify_checksum(&cache_path, checksum).is_ok() {
           Some(cache_path)
       } else {
           None
       }
   }

**Benefit:** Skip re-downloading large model files if already present (saves bandwidth and time)

Security Considerations
-----------------------

Checksum Verification
~~~~~~~~~~~~~~~~~~~~~

**All downloaded files MUST be verified** with SHA-256 checksums:

.. code:: rust

   pub fn verify_checksum(file_path: &Path, expected: &str) -> Result<()> {
       let mut file = File::open(file_path)?;
       let mut hasher = Sha256::new();
       std::io::copy(&mut file, &mut hasher)?;
       let actual = format!("{:x}", hasher.finalize());

       if actual != expected {
           return Err(Error::ChecksumMismatch {
               file: file_path.display().to_string(),
               expected: expected.to_string(),
               actual,
           });
       }

       Ok(())
   }

Temporary File Security
~~~~~~~~~~~~~~~~~~~~~~~

**Temporary files MUST have restrictive permissions:**

.. code:: rust

   use std::os::unix::fs::PermissionsExt;

   pub fn create_temp_file() -> Result<File> {
       let file = tempfile::NamedTempFile::new()?;

       #[cfg(unix)]
       {
           let mut perms = file.as_file().metadata()?.permissions();
           perms.set_mode(0o600);  // User read/write only
           file.as_file().set_permissions(perms)?;
       }

       Ok(file)
   }

No Arbitrary Code Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Manifests MUST NOT allow arbitrary code execution:**

- NO ``eval()`` or similar dynamic execution
- Build commands are templated strings, not code
- Install steps are data structures, not scripts

Testing Strategy
----------------

Unit Tests
~~~~~~~~~~

**Coverage:** Each module (manifest, components, packager, installer)

**Example:**

.. code:: rust

   #[cfg(test)]
   mod tests {
       use super::*;

       #[test]
       fn test_manifest_parse_valid() {
           let toml = r#"
               [package]
               name = "test"
               version = "1.0.0"
               description = "Test package"
           "#;

           let manifest: Manifest = toml::from_str(toml).unwrap();
           assert_eq!(manifest.package.name, "test");
       }

       #[test]
       fn test_checksum_verification() {
           // Create test file with known content
           // Verify correct checksum passes
           // Verify incorrect checksum fails
       }
   }

Integration Tests
~~~~~~~~~~~~~~~~~

**Scenario:** End-to-end package creation and installation

.. code:: rust

   #[test]
   fn test_whisper_lite_packaging() {
       // Create minimal AirGapDeploy.toml for test app
       // Run `airgap-deploy prep`
       // Verify package structure
       // Extract package in temp directory
       // Run install script in test environment
       // Verify installation succeeded
   }

Platform Testing
~~~~~~~~~~~~~~~~

**CI Matrix:**

- Linux: Ubuntu 20.04, Ubuntu 22.04, Fedora 38
- macOS: macOS 12 (Intel), macOS 14 (Apple Silicon)
- Windows: Windows 10, Windows 11

Future Enhancements
-------------------

Pre-built Binaries (v0.2)
~~~~~~~~~~~~~~~~~~~~~~~~~

Add ``prebuild = true`` option to build binaries on developer machine:

.. code:: toml

   [[components]]
   type = "rust-app"
   source = "."
   prebuild = true
   target = "x86_64-unknown-linux-gnu"

**Requires:** Cross-compilation toolchain setup

Digital Signatures (v1.1)
~~~~~~~~~~~~~~~~~~~~~~~~~

Sign packages for verification on air-gapped systems:

.. code:: bash

   airgap-deploy prep --sign-with ~/.gnupg/key.asc

**Requires:** GPG integration, key management

Plugin System (v2.0)
~~~~~~~~~~~~~~~~~~~~

See :doc:`Roadmap <../roadmap>` (Phase 7)
