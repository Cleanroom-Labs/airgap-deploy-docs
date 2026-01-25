AirGap Deploy
=============

A command-line tool for packaging applications and their dependencies for deployment on air-gapped systems.

Features
--------

- **Declarative manifests** - Define deployments in simple TOML files
- **Cross-platform** - Works on Linux, macOS, and Windows
- **Component-based** - Package Rust apps, binaries, models, and system packages
- **Automated installation** - Generates platform-specific install scripts
- **Offline-ready** - Everything needed for air-gap deployment in one package

How It Works
------------

Deploy any application to air-gapped systems in two phases:

**Phase 1 - Preparation (Connected System):**

Create ``AirGapDeploy.toml`` manifest defining your application
Run ``airgap-deploy prep`` to download and package everything
Transfer package via USB or other physical media

**Phase 2 - Installation (Air-Gapped System):**

Extract package on air-gapped system
Run generated ``install.sh`` (or ``install.ps1`` on Windows)
Installation script builds and installs everything offline

No network required on the air-gapped system.

Quick Start
-----------

Prerequisites
~~~~~~~~~~~~~

- Rust toolchain (for building airgap-deploy)
- Internet access (for preparation phase)
- Git (for cloning external repositories)

Installation
~~~~~~~~~~~~

Build from source with Cargo:

.. code:: bash

   cargo install airgap-deploy

Or use a pre-built binary for your platform.

First Deployment
~~~~~~~~~~~~~~~~

Create a manifest for your application:

.. code:: toml

   # AirGapDeploy.toml
   [package]
   name = "my-app"
   version = "1.0.0"
   description = "My application for air-gap deployment"

   [[components]]
   type = "rust-app"
   source = "."
   vendor = true
   include_toolchain = true

   [install]
   method = "build-from-source"
   install_to = "user"
   mode = "interactive"

Prepare the deployment package:

.. code:: bash

   airgap-deploy prep --output dist/my-app.tar.gz

Transfer to air-gapped system and install:

.. code:: bash

   # On air-gapped system
   tar -xzf my-app.tar.gz
   cd my-app
   ./install.sh

Usage
-----

Preparing Packages
~~~~~~~~~~~~~~~~~~

Create deployment packages on connected systems:

.. code:: bash

   # Use manifest in current directory
   airgap-deploy prep

   # Specify manifest location
   airgap-deploy prep --manifest path/to/AirGapDeploy.toml

   # Specify target platform
   airgap-deploy prep --target linux-x86_64

   # Specify output location
   airgap-deploy prep --output dist/package.tar.gz

   # Dry run (preview without creating package)
   airgap-deploy prep --dry-run

Validating Manifests
~~~~~~~~~~~~~~~~~~~~

Validate manifest syntax before packaging:

.. code:: bash

   airgap-deploy validate
   airgap-deploy validate --manifest AirGapDeploy.toml

Creating Manifests
~~~~~~~~~~~~~~~~~~

Generate template manifests:

.. code:: bash

   # Generic template
   airgap-deploy init

   # Rust application template
   airgap-deploy init --type rust-app

   # Python application template
   airgap-deploy init --type python-app

Listing Components
~~~~~~~~~~~~~~~~~~

Show available component types:

.. code:: bash

   airgap-deploy list-components

Manifest Reference
------------------

Package Section
~~~~~~~~~~~~~~~

.. code:: toml

   [package]
   name = "app-name"           # Required: Package name
   version = "1.0.0"           # Required: Version
   description = "..."         # Required: Description

Targets Section
~~~~~~~~~~~~~~~

.. code:: toml

   [targets]
   platforms = ["linux-x86_64", "macos-aarch64", "windows-x86_64"]
   default = "linux-x86_64"

Components
~~~~~~~~~~

Rust Application
^^^^^^^^^^^^^^^^

.. code:: toml

   [[components]]
   type = "rust-app"
   source = "."                # Path to Cargo project
   vendor = true               # Vendor dependencies
   include_toolchain = true    # Include Rust installer

External Binary
^^^^^^^^^^^^^^^

.. code:: toml

   [[components]]
   type = "external-binary"
   name = "whisper.cpp"
   repo = "https://github.com/ggerganov/whisper.cpp.git"
   tag = "v1.0.0"              # Or: branch = "main", commit = "abc123"
   build_instructions = "make"

Model File
^^^^^^^^^^

.. code:: toml

   [[components]]
   type = "model-file"
   name = "base.en"
   url = "https://example.com/model.bin"
   checksum = "sha256:abc123..."
   required = true             # Default: true
   install_path = "models/model.bin"

System Package
^^^^^^^^^^^^^^

.. code:: toml

   [[components]]
   type = "system-package"
   name = "alsa"
   packages = ["libasound2-dev"]  # Debian/Ubuntu
   platforms = ["linux"]

**Note:** SystemPackageComponent deferred to v0.2

Installation Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: toml

   [install]
   method = "build-from-source"    # Or: "prebuilt-binary"
   install_to = "user"             # Or: "system"
   mode = "interactive"            # Or: "automatic"

   # Optional: Custom install steps
   [install.steps]
   step_name = [
       "command1",
       "command2"
   ]

   # Optional: Configuration template
   [install.config]
   config_file = "~/.config/app/config.toml"
   config_template = """
   app_path = "{{ install_prefix }}"
   """

Examples
--------

Example 1: Rust Application with Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: toml

   [package]
   name = "airgap-whisper"
   version = "0.1.0"
   description = "Offline audio transcription"

   [[components]]
   type = "rust-app"
   source = "."
   vendor = true
   include_toolchain = true

   [[components]]
   type = "external-binary"
   name = "whisper.cpp"
   repo = "https://github.com/ggerganov/whisper.cpp.git"
   tag = "v1.0.0"
   build_instructions = "make"

   [[components]]
   type = "model-file"
   name = "base.en"
   url = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin"
   checksum = "sha256:..."

   [install]
   method = "build-from-source"
   install_to = "user"

Example 2: Large ML Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: toml

   [package]
   name = "ollama-deploy"
   version = "0.15.0"
   description = "Ollama runtime with models"

   [[components]]
   type = "external-binary"
   name = "ollama"
   repo = "https://github.com/ollama/ollama.git"
   tag = "v0.15.0"
   build_instructions = "make"

   [[components]]
   type = "model-file"
   name = "llama2-7b"
   url = "https://ollama.ai/download/llama2-7b.gguf"
   checksum = "sha256:..."

   [install]
   method = "build-from-source"
   install_to = "user"

Integration with airgap-transfer
--------------------------------

For large packages that exceed USB capacity, use airgap-transfer:

.. code:: bash

   # Create large package
   airgap-deploy prep --manifest AirGapDeploy.ollama.toml
   # Output: ollama-deploy-20GB.tar.gz

   # Chunk for multiple USB drives
   airgap-transfer pack ollama-deploy-20GB.tar.gz /media/usb --chunk-size 16GB

   # Transfer chunks across air-gap

   # Reconstruct on air-gapped system
   airgap-transfer unpack /media/usb ~/deployment/

   # Install as normal
   cd ~/deployment/ollama-deploy
   ./install.sh

See :doc:`airgap-transfer documentation </airgap-transfer/readme>` for details.

Platform Support
----------------

======== ======= ================================================
Platform Support Notes
======== ======= ================================================
Linux    Full    Tested on Ubuntu 20.04+, Fedora 35+, Debian 11+
macOS    Full    Tested on macOS 10.15+ (Intel and Apple Silicon)
Windows  Full    Tested on Windows 10/11
======== ======= ================================================

**Generated install scripts:**

- Linux/macOS: Bash 4.0+
- Windows: PowerShell 5.1+

Building
--------

Requires Rust toolchain and platform-specific build tools.

See :doc:`Roadmap <roadmap>` for complete build instructions.

Documentation
-------------

This README covers installation and usage. For development and technical specifications, see the documents below.

Start Here
~~~~~~~~~~

+---------------------------------------------+-------------------------------------+
| Document                                    | Purpose                             |
+=============================================+=====================================+
| :doc:`Principles </meta/principles>`        | Core design principles (read first) |
+---------------------------------------------+-------------------------------------+
| :doc:`Roadmap <roadmap>`                    | Project status and direction        |
+---------------------------------------------+-------------------------------------+

Technical Documentation
~~~~~~~~~~~~~~~~~~~~~~~

+----------------------------------------------+--------------------------------------------+
| Document                                     | Purpose                                    |
+==============================================+============================================+
| :doc:`Requirements (SRS) <requirements/srs>` | Detailed functional requirements           |
+----------------------------------------------+--------------------------------------------+
| :doc:`Design (SDD) <design/sdd>`             | Architecture, component design, algorithms |
+----------------------------------------------+--------------------------------------------+
| :doc:`Test Plan <testing/plan>`              | Test cases and procedures                  |
+----------------------------------------------+--------------------------------------------+

Project Planning
~~~~~~~~~~~~~~~~

+--------------------------------------------+---------------------------------+
| Document                                   | Purpose                         |
+============================================+=================================+
| :doc:`Roadmap <roadmap>`                   | 7-phase implementation plan     |
+--------------------------------------------+---------------------------------+
| :doc:`Use Case Analysis <use-cases/index>` | Workflow documentation          |
+--------------------------------------------+---------------------------------+

Meta-Architecture
~~~~~~~~~~~~~~~~~

+---------------------------------------------------------------+----------------------------------------------------+
| Document                                                      | Purpose                                            |
+===============================================================+====================================================+
| :doc:`Meta-Architecture </meta/meta-architecture>`            | How airgap-deploy relates to other AirGap projects |
+---------------------------------------------------------------+----------------------------------------------------+
| `Requirements Overview <../meta/requirements-overview.rst>`__ | Project statistics and requirements overview       |
+---------------------------------------------------------------+----------------------------------------------------+

Use Cases
---------

airgap-deploy is designed for:

- **Release engineers** packaging applications for air-gapped deployment
- **DevOps teams** deploying to isolated environments
- **Security-conscious organizations** requiring offline installation
- **Developers** creating reproducible deployment packages

**Primary use case:** Package Cleanroom Whisper and similar applications for air-gapped systems.

Privacy
-------

airgap-deploy operates in two distinct phases:

- **Preparation phase (connected):** Downloads components, creates package
- **Installation phase (air-gapped):** No network access required or attempted

Generated installation scripts are completely offline.

.. _airgap-deploy-readme-competition:

Why AirGap Deploy?
------------------

AirGap Deploy fills the gap for **lightweight, general-purpose application packaging** for air-gapped systems. While other tools focus on specific deployment targets, AirGap Deploy is designed for desktop applications, simple binaries, and Rust ecosystem projects.

**vs Kubernetes tools** (`Zarf <https://github.com/defenseunicorns/zarf>`__, `UDS <https://uds.defenseunicorns.com/>`__, KOSI):

- ✅ **Desktop application focus**: No Kubernetes cluster required
- ✅ **Simple TOML manifests**: Human-readable, easy to version control
- ✅ **Minimal infrastructure**: Single Rust binary, no runtime dependencies
- ✅ **Direct binary deployment**: Native applications, not containerized workloads

**vs container platforms** (`Docker <https://www.docker.com/>`__, Podman):

- ✅ **No runtime requirements**: No Docker daemon needed on target system
- ✅ **Native performance**: Direct binary execution, not virtualized
- ✅ **Rust ecosystem integration**: First-class support for cargo vendoring
- ✅ **Model file support**: Built-in handling for ML/AI model downloads

**vs enterprise tools** (`JFrog Artifactory <https://jfrog.com/artifactory/>`__, `Commvault <https://www.commvault.com/>`__):

- ✅ **Free and open source**: No licensing costs or vendor lock-in
- ✅ **Lightweight**: No heavy infrastructure (Artifactory, registries, databases)
- ✅ **Simple workflow**: Manifest → package → install script, nothing more
- ✅ **Developer-friendly**: Designed for release engineers, not enterprise IT

**vs language-specific tools** (`pip download <https://pip.pypa.io/en/stable/cli/pip_download/>`__, `cargo-vendor <https://doc.rust-lang.org/cargo/commands/cargo-vendor.html>`__, `conda pack <https://conda.github.io/conda-pack/>`__):

- ✅ **Multi-component support**: Package apps + binaries + models + packages
- ✅ **Cross-platform installation scripts**: Bash (Linux/macOS) and PowerShell (Windows)
- ✅ **Dependency verification**: SHA-256 checksums for all components
- ✅ **Automated builds**: Installation scripts handle building from source offline

**Unique value proposition:** The only tool designed specifically for packaging Rust applications with ML models (like Cleanroom Whisper + whisper.cpp + model files) for air-gapped desktop deployment.

**Complementary to Zarf:** Use Zarf for Kubernetes workloads, AirGap Deploy for desktop applications. Both solve air-gap deployment, different targets.

License
-------

Dual-licensed under MIT OR Apache-2.0 (your choice).

Contributing
------------

See :doc:`Roadmap <roadmap>` for architecture and implementation details.

Roadmap
-------

See :doc:`Roadmap <roadmap>` for current status and future plans.
