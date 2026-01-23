Use Case Analysis
=================

Primary Use Case: AirGap Whisper Deployment
-------------------------------------------

Current Design Coverage
~~~~~~~~~~~~~~~~~~~~~~~

+-------------------------------------+-----------------------------+--------------+--------------------------------------+
| Requirement                         | Component                   | Status       | Notes                                |
+=====================================+=============================+==============+======================================+
| Package Rust source + vendored deps | ``RustAppComponent``        | ✅ Supported | ``vendor = true``                    |
+-------------------------------------+-----------------------------+--------------+--------------------------------------+
| Include Rust toolchain installer    | ``RustAppComponent``        | ✅ Supported | ``include_toolchain = true``         |
+-------------------------------------+-----------------------------+--------------+--------------------------------------+
| Package whisper.cpp source          | ``ExternalBinaryComponent`` | ✅ Supported | Git clone                            |
+-------------------------------------+-----------------------------+--------------+--------------------------------------+
| Download Whisper models             | ``ModelFileComponent``      | ✅ Supported | With checksums                       |
+-------------------------------------+-----------------------------+--------------+--------------------------------------+
| Include ALSA packages (Linux)       | ``SystemPackageComponent``  | ⚠️ Partial   | Exists but not in example            |
+-------------------------------------+-----------------------------+--------------+--------------------------------------+
| Multi-platform packages             | Platform abstraction        | ⚠️ Deferred  | Cross-compilation in v0.2            |
+-------------------------------------+-----------------------------+--------------+--------------------------------------+
| Installation script generation      | Template system             | ✅ Supported | Bash/PowerShell                      |
+-------------------------------------+-----------------------------+--------------+--------------------------------------+
| Post-install configuration          | Install steps               | ❌ **Gap**   | No mechanism defined                 |
+-------------------------------------+-----------------------------+--------------+--------------------------------------+
| Interactive installation            | Install scripts             | ❌ **Gap**   | Not specified                        |
+-------------------------------------+-----------------------------+--------------+--------------------------------------+
| Multiple model selection            | Manifest                    | ⚠️ Unclear   | Can add multiple components, but UX? |
+-------------------------------------+-----------------------------+--------------+--------------------------------------+

Critical Gaps Identified
~~~~~~~~~~~~~~~~~~~~~~~~

Gap 1: Post-Installation Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem:** AirGap Whisper needs to know where whisper.cpp and models are installed.

**Current Plan:** No mechanism for post-install configuration.

**Solution:**

.. code:: toml

   [install.config]
   config_file = "~/.config/airgap-whisper/config.toml"
   config_template = """
   # AirGap Whisper auto-discovers binary and models from this path
   whisper_path = "{{ install_prefix }}"
   """

**Install script should:**

Build and install whisper.cpp to known location
Copy all models to known location (``{{ install_prefix }}/share/airgap-whisper/models/``)
Generate config file with install prefix
Install AirGap Whisper binary

**AirGap Whisper runtime auto-discovery:**

- Binary: Search ``whisper_path/bin/`` for ``whisper-main``, ``main``, ``whisper-cli``, etc.
- Models: Scan ``whisper_path/share/airgap-whisper/models/*.bin``
- No need for explicit paths in config

Gap 2: Multiple Model Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem:** Users may want different model sizes (tiny, base, small, medium, large).

**Current Plan:** Can list multiple ``[[components]]`` of type ``model-file``, but:

- All models included = large package (3+ GB)
- No way to make models optional/selectable

**Options:**

**Option A: Multiple Manifests**

.. code:: bash

   # Developer creates multiple packages
   airgap-deploy prep --manifest AirGapDeploy.base.toml   # Just base.en (140MB)
   airgap-deploy prep --manifest AirGapDeploy.full.toml   # All models (3GB)

**Option B: Component Selection at Prep Time**

.. code:: toml

   [[components]]
   type = "model-file"
   name = "base.en"
   url = "..."
   required = true  # Always included

   [[components]]
   type = "model-file"
   name = "small.en"
   url = "..."
   required = false  # Optional, include with --include small.en

.. code:: bash

   airgap-deploy prep --include small.en --include medium.en

**Option C: Interactive Installation**

.. code:: bash

   # Install script prompts:
   # "Which models do you want to install?"
   # [x] base.en (140MB) - Recommended
   # [ ] small.en (460MB)
   # [ ] medium.en (1.5GB)

Gap 3: Cross-Platform Packaging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem:** Developer on macOS wants to create packages for Linux and Windows.

**Current Plan:** Deferred to v0.2 (cross-compilation).

**Impact:** Developer must:

- Run AirGap Deploy on each target platform, OR
- Use CI/CD with multiple platform runners, OR
- Wait for v0.2

**Recommendation:** This is acceptable for v0.1, use GitHub Actions matrix builds.

Gap 4: Installation Locations & Permissions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem:** Where do things get installed?

**Current Plan:**

.. code:: toml

   [install]
   install_to = "user"  # or "system"

**Questions:**

- User install: ``~/.local/bin`` (Linux/macOS), ``%LOCALAPPDATA%\Programs`` (Windows)?
- System install: ``/usr/local/bin`` (needs sudo)?
- Models: ``~/.local/share/airgap-whisper/models`` or ``/usr/share/airgap-whisper/models``?
- Config: ``~/.config/airgap-whisper/config.toml`` or ``/etc/airgap-whisper/config.toml``?

**Needed:** Platform-specific path resolution in install scripts.

Gap 5: Dependency Verification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Problem:** Install script should verify dependencies before building.

**Current Plan:** Mentioned in Phase 4 (“Dependency checking”), but not detailed.

**Needed:**

.. code:: bash

   # Generated install script should check:
   - Rust toolchain (or install from included installer)
   - C compiler (gcc/clang/MSVC) for whisper.cpp
   - make (for whisper.cpp build)
   - ALSA headers (on Linux, from included .deb/.rpm)
   - Sufficient disk space

--------------

Use Case Matrix
---------------

Use Case 1: Developer Creating Release (Primary)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Actor:** AirGap Whisper maintainer **Environment:** macOS laptop with internet **Goal:** Create release packages for Linux, macOS, Windows

**Workflow:**

Update ``AirGapDeploy.toml`` with new version
Run CI/CD that executes on Linux, macOS, Windows runners:

   .. code:: yaml

      - name: Package for air-gap
        run: airgap-deploy prep --target ${{ matrix.platform }} --output dist/

Upload artifacts to GitHub releases
Users download pre-built packages

**Current Plan Support:** ✅ Fully supported (with GitHub Actions)

--------------

Use Case 2: End User Installing on Air-Gapped System (Primary)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Actor:** Security researcher on air-gapped workstation **Environment:** Ubuntu 22.04 with no internet, ALSA installed **Goal:** Install and run AirGap Whisper

**Workflow:**

Download ``airgap-whisper-linux-x86_64.tar.gz`` via USB
Extract: ``tar -xzf airgap-whisper-linux-x86_64.tar.gz``
Run: ``cd airgap-whisper-linux-x86_64 && ./install.sh``
Install script:

   - Checks Rust (installs from included installer if missing)
   - Checks ALSA (installs from included .deb if missing)
   - Builds whisper.cpp
   - Builds airgap-whisper
   - Installs to ``~/.local/bin``
   - Generates ``~/.config/airgap-whisper/config.toml``

Run: ``airgap-whisper``

**Current Plan Support:** ⚠️ Mostly supported, gaps in config generation

--------------

Use Case 3: Advanced User Custom Build (Secondary)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Actor:** Developer customizing AirGap Whisper **Environment:** Arch Linux with internet **Goal:** Create custom package with specific models

**Workflow:**

Clone airgap-whisper repo
Edit ``AirGapDeploy.toml`` to include only desired models
Run: ``airgap-deploy prep --target linux-x86_64``
Transfer to air-gapped system
Install as normal

**Current Plan Support:** ✅ Fully supported

--------------

Use Case 4: Enterprise Deployment (Future)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Actor:** IT admin deploying to 100 air-gapped workstations **Environment:** Mixed Windows/Linux fleet **Goal:** Automated installation without interaction

**Workflow:**

Download pre-built packages
Create deployment script:

   .. code:: bash

      # Unattended install
      ./install.sh --non-interactive --prefix /opt/airgap-whisper

Deploy via configuration management (Ansible, GPO, etc.)

**Current Plan Support:** ❌ Not supported (no unattended install mode)

--------------

Architectural Recommendations
-----------------------------

Recommendation 1: Add Post-Install Configuration with Auto-Discovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Extend Manifest:**

.. code:: toml

   [install]
   method = "build-from-source"
   install_to = "user"  # or "system"

   # Simple post-install configuration - let app auto-discover details
   [install.config]
   config_file = "~/.config/airgap-whisper/config.toml"
   config_template = """
   # AirGap Whisper auto-discovers binary and models from this path
   whisper_path = "{{ install_prefix }}"

   [audio]
   sample_rate = 16000
   channels = 1
   """

   # Custom installation steps
   [install.steps]
   whisper_cpp = [
       "cd whisper.cpp",
       "make",
       "mkdir -p {{ install_prefix }}/bin",
       "cp main {{ install_prefix }}/bin/whisper-main"
   ]
   models = [
       "mkdir -p {{ install_prefix }}/share/airgap-whisper/models",
       "cp models/*.bin {{ install_prefix }}/share/airgap-whisper/models/"
   ]
   airgap_whisper = [
       "cd airgap-whisper",
       "cargo build --release --offline",
       "cp target/release/airgap-whisper {{ install_prefix }}/bin/"
   ]

**AirGap Whisper Auto-Discovery:**

- Discovers whisper binary by searching ``whisper_path/bin/`` for known names
- Discovers all models by scanning ``whisper_path/share/airgap-whisper/models/*.bin``
- No explicit paths needed in config, improving UX

**Implementation:** Phase 4 (Install Script Generation)

--------------

Recommendation 2: Optional Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Extend Component Definition:**

.. code:: toml

   [[components]]
   type = "model-file"
   name = "base.en"
   url = "https://huggingface.co/..."
   checksum = "sha256:..."
   required = true  # Always included
   default = true

   [[components]]
   type = "model-file"
   name = "small.en"
   url = "https://huggingface.co/..."
   checksum = "sha256:..."
   required = false  # Optional
   default = false

**CLI:**

.. code:: bash

   # Include optional components
   airgap-deploy prep --include small.en --include medium.en

   # Or use interactive mode
   airgap-deploy prep --interactive
   # Prompts: "Include small.en (460MB)? [y/N]"

**Implementation:** Phase 2 (Component System)

--------------

Recommendation 3: Installation Modes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Extend Install Configuration:**

.. code:: toml

   [install]
   method = "build-from-source"
   install_to = "user"
   mode = "interactive"  # or "automatic"

   # Interactive prompts
   [install.prompts]
   install_location = "Where should AirGap Whisper be installed?"
   install_location_default = "~/.local"
   install_system_wide = "Install system-wide (requires sudo)?"
   install_system_wide_default = false

**Generated Install Script:**

.. code:: bash

   #!/bin/bash
   set -e

   # Installation mode
   MODE="${MODE:-interactive}"

   if [ "$MODE" = "interactive" ]; then
       read -p "Where should AirGap Whisper be installed? [~/.local]: " INSTALL_PREFIX
       INSTALL_PREFIX="${INSTALL_PREFIX:-$HOME/.local}"
   else
       INSTALL_PREFIX="${INSTALL_PREFIX:-$HOME/.local}"
   fi

   # Non-interactive mode for enterprise
   # ./install.sh MODE=automatic INSTALL_PREFIX=/opt/airgap-whisper

**Implementation:** Phase 4 (Install Script Generation)

--------------

Recommendation 4: Dependency Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Install Script Should Check:**

.. code:: bash

   #!/bin/bash
   set -e

   echo "=== AirGap Whisper Installation ==="
   echo

   # Check for required tools
   echo "Checking dependencies..."

   # Check Rust
   if ! command -v rustc &> /dev/null; then
       echo "  Installing Rust toolchain..."
       cd rust-installer && ./install.sh --prefix=$INSTALL_PREFIX
   fi

   # Check C compiler (for whisper.cpp)
   if ! command -v gcc &> /dev/null && ! command -v clang &> /dev/null; then
       echo "ERROR: C compiler not found. Please install gcc or clang."
       exit 1
   fi

   # Check make
   if ! command -v make &> /dev/null; then
       echo "ERROR: make not found. Please install make."
       exit 1
   fi

   # Linux: Check ALSA
   if [ "$(uname)" = "Linux" ]; then
       if ! ldconfig -p | grep -q libasound; then
           echo "  Installing ALSA libraries..."
           # Install from included .deb/.rpm
       fi
   fi

   # Check disk space
   REQUIRED_SPACE=500000  # 500MB in KB
   AVAILABLE_SPACE=$(df "$INSTALL_PREFIX" | tail -1 | awk '{print $4}')
   if [ "$AVAILABLE_SPACE" -lt "$REQUIRED_SPACE" ]; then
       echo "ERROR: Insufficient disk space. Need 500MB, have $(($AVAILABLE_SPACE/1024))MB"
       exit 1
   fi

   echo "All dependencies satisfied."
   echo

**Implementation:** Phase 4 (Install Script Generation)

--------------

Phase Priority Adjustments
--------------------------

Given the gaps, I recommend adjusting the MVP scope:

Current MVP (v0.1.0)
~~~~~~~~~~~~~~~~~~~~

- ✅ Phase 1: Core infrastructure
- ✅ Phase 2: Built-in components (RustApp, ExternalBinary, ModelFile)
- ✅ Phase 3: Packaging
- ✅ Phase 4: Install scripts (basic)
- ✅ Phase 5: Basic CLI
- ❌ Phase 6: Partial tests/docs
- ❌ Phase 7: Plugin system (skip)

Recommended MVP (v0.1.0)
~~~~~~~~~~~~~~~~~~~~~~~~

- ✅ Phase 1: Core infrastructure
- ✅ Phase 2: Built-in components + **optional components**
- ✅ Phase 3: Packaging
- ✅ Phase 4: Install scripts + **config generation** + **dependency checks** + **installation modes**
- ✅ Phase 5: Basic CLI + **–include flag**
- ❌ Phase 6: Partial tests/docs
- ❌ Phase 7: Plugin system (skip)
- ❌ SystemPackageComponent (defer to v0.2)

**Rationale:** Post-install configuration and dependency checking are critical for the AirGap Whisper use case to work smoothly.

--------------

Example: Complete AirGap Whisper Manifest
-----------------------------------------

.. code:: toml

   [package]
   name = "airgap-whisper"
   version = "0.1.0"
   description = "Offline audio transcription"

   [targets]
   platforms = ["linux-x86_64", "macos-aarch64", "windows-x86_64"]
   default = "linux-x86_64"

   # Rust application
   [[components]]
   type = "rust-app"
   source = "."
   vendor = true
   include_toolchain = true
   prebuild = false  # Build on target system

   # whisper.cpp dependency
   [[components]]
   type = "external-binary"
   name = "whisper.cpp"
   repo = "https://github.com/ggerganov/whisper.cpp.git"
   branch = "master"
   build_instructions = "make"

   # Models (base is required, others optional)
   [[components]]
   type = "model-file"
   name = "base.en"
   url = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin"
   checksum = "sha256:..."
   size = "140MB"
   required = true
   default = true

   [[components]]
   type = "model-file"
   name = "small.en"
   url = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin"
   checksum = "sha256:..."
   size = "460MB"
   required = false
   default = false

   [[components]]
   type = "model-file"
   name = "medium.en"
   url = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.en.bin"
   checksum = "sha256:..."
   size = "1.5GB"
   required = false
   default = false

   # Installation configuration
   [install]
   method = "build-from-source"
   install_to = "user"  # ~/.local on Linux/macOS, %LOCALAPPDATA% on Windows
   mode = "interactive"

   # Post-install configuration
   # AirGap Whisper will automatically discover models and binary from whisper_path
   [install.config]
   config_file = "~/.config/airgap-whisper/config.toml"
   config_template = """
   # AirGap Whisper looks for whisper.cpp installation here
   # The tool will automatically discover:
   #   - Binary: <whisper_path>/bin/whisper-main (or main, whisper-cli)
   #   - Models: <whisper_path>/share/airgap-whisper/models/*.bin
   whisper_path = "{{ install_prefix }}"

   [audio]
   sample_rate = 16000
   channels = 1

   [hotkeys]
   record = "Ctrl+Alt+R"
   copy_last = "Ctrl+Alt+C"
   """

   # Custom installation steps
   [install.steps]
   whisper_cpp = [
       "cd whisper.cpp",
       "make",
       "mkdir -p {{ install_prefix }}/bin",
       "cp main {{ install_prefix }}/bin/whisper-main",
   ]

   models = [
       "mkdir -p {{ install_prefix }}/share/airgap-whisper/models",
       "cp models/*.bin {{ install_prefix }}/share/airgap-whisper/models/",
   ]

   airgap_whisper = [
       "cd airgap-whisper",
       "cargo build --release --offline",
       "mkdir -p {{ install_prefix }}/bin",
       "cp target/release/airgap-whisper {{ install_prefix }}/bin/",
   ]

   config = [
       "mkdir -p ~/.config/airgap-whisper",
       "# Config file already generated by template",
   ]

   # Dependency verification
   [install.dependencies]
   rust = { required = true, install_if_missing = true }
   gcc = { required = true, install_if_missing = false }
   make = { required = true, install_if_missing = false }

   [install.dependencies.linux]
   alsa = { required = true, install_if_missing = true, packages = ["libasound2-dev"] }

AirGap Whisper Runtime Behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With this simpler configuration, AirGap Whisper’s runtime logic:

.. code:: rust

   // src/whisper.rs - AirGap Whisper code

   pub struct WhisperConfig {
       pub whisper_path: PathBuf,
       // Binary and models auto-discovered
   }

   impl WhisperConfig {
       pub fn from_config_file() -> Result<Self> {
           let config = read_config("~/.config/airgap-whisper/config.toml")?;
           Ok(Self {
               whisper_path: config.whisper_path,
           })
       }

       /// Auto-discover whisper binary
       pub fn binary_path(&self) -> Result<PathBuf> {
           // Try common binary names in order
           for name in ["whisper-main", "main", "whisper-cli", "whisper"] {
               let path = self.whisper_path.join("bin").join(name);
               if path.exists() {
                   return Ok(path);
               }
           }
           Err(Error::WhisperBinaryNotFound)
       }

       /// Auto-discover all available models
       pub fn available_models(&self) -> Result<Vec<ModelInfo>> {
           let models_dir = self.whisper_path.join("share/airgap-whisper/models");
           let mut models = Vec::new();

           for entry in std::fs::read_dir(models_dir)? {
               let entry = entry?;
               let path = entry.path();

               // Find all .bin files
               if path.extension() == Some(OsStr::new("bin")) {
                   let name = path.file_stem()
                       .and_then(|s| s.to_str())
                       .ok_or(Error::InvalidModelName)?;

                   models.push(ModelInfo {
                       name: name.to_string(),
                       path: path.clone(),
                       size: std::fs::metadata(&path)?.len(),
                   });
               }
           }

           Ok(models)
       }

       /// Get default model (first available, or user-specified)
       pub fn default_model(&self) -> Result<PathBuf> {
           let models = self.available_models()?;
           models.first()
               .map(|m| m.path.clone())
               .ok_or(Error::NoModelsFound)
       }
   }

**Benefits:**

- User only specifies one path: ``whisper_path``
- All models in models directory are automatically available
- No need to update config when adding new models
- Binary name detection handles different whisper.cpp versions
- Simpler mental model for users

--------------

Summary
-------

Does Current Plan Support AirGap Whisper?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Yes, but with critical gaps:**

✅ **Supported:**

- Packaging Rust app with vendored dependencies
- Including Rust toolchain
- Packaging external binaries (whisper.cpp)
- Downloading models with verification
- Generating installation scripts
- Multi-platform targeting (with CI/CD)

❌ **Gaps:**

- Post-installation configuration generation
- Optional component selection
- Dependency verification in install scripts
- Interactive vs. automated installation modes
- Cross-platform packaging from single system (deferred)

Recommended Actions
~~~~~~~~~~~~~~~~~~~

**Immediate (Phase 1-2):** Add optional component support to manifest schema
**Phase 4 Enhancement:** Implement config generation, dependency checks, installation modes
**Documentation:** Create complete AirGap Whisper example in ``examples/airgap-whisper/``
**Testing:** Validate on actual air-gapped VMs before v0.1.0 release

The foundation is solid, but these enhancements are needed for a smooth AirGap Whisper deployment experience.
