Use Case: Cleanroom Whisper Deployment
=======================================

This document describes the complete end-to-end workflow for packaging and deploying Cleanroom Whisper using AirGap Deploy.

Overview
--------

The workflow has two sides:

**Developer Side** (Connected System) - Creating release packages
**User Side** (Air-Gapped System) - Installing from package

.. usecase:: Cleanroom Whisper Deployment Workflow
   :id: UC-DEPLOY-001
   :status: approved
   :tags: deploy, workflow, cleanroom-whisper
   :release: v1.0

   Complete end-to-end workflow for packaging Cleanroom Whisper with AirGap Deploy and deploying to air-gapped systems.

   **Developer Side:** Create multi-platform release packages using GitHub Actions, vendor all dependencies, include Rust toolchain and whisper.cpp source.

   **User Side:** Transfer package via USB, run installation script to build and install on air-gapped system with minimal interaction.

   **Success Criteria:** Developer creates releases with single git tag push; user installs with single script execution; complete offline functionality.

--------------

Developer Workflow: Creating Release Packages
---------------------------------------------

Prerequisites
~~~~~~~~~~~~~

- Development machine with internet access
- Git repository cloned
- AirGap Deploy installed (``cargo install airgap-deploy``)
- Access to GitHub repository (for releases)

Step 1: Prepare AirGapDeploy.toml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: toml

   [package]
   name = "cleanroom-whisper"
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

   # whisper.cpp dependency
   [[components]]
   type = "external-binary"
   name = "whisper.cpp"
   repo = "https://github.com/ggerganov/whisper.cpp.git"
   build_instructions = "make"

   # Whisper model (base.en)
   [[components]]
   type = "model-file"
   name = "base.en"
   url = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin"
   checksum = "sha256:..."
   required = true

   # Installation configuration
   [install]
   method = "build-from-source"
   install_to = "user"
   mode = "interactive"

   # Simple configuration: Cleanroom Whisper auto-discovers binary and models
   [install.config]
   config_file = "~/.config/cleanroom-whisper/config.toml"
   config_template = """
   # Cleanroom Whisper auto-discovers whisper binary and all models from this path
   whisper_path = "{{ install_prefix }}"

   [audio]
   sample_rate = 16000
   channels = 1

   [hotkeys]
   record = "Ctrl+Alt+R"
   copy_last = "Ctrl+Alt+C"
   """

   [install.steps]
   whisper_cpp = [
       "cd whisper.cpp",
       "make",
       "mkdir -p {{ install_prefix }}/bin",
       "cp main {{ install_prefix }}/bin/whisper-main"
   ]
   models = [
       "mkdir -p {{ install_prefix }}/share/cleanroom-whisper/models",
       "cp models/*.bin {{ install_prefix }}/share/cleanroom-whisper/models/"
   ]
   cleanroom_whisper = [
       "cd cleanroom-whisper",
       "cargo build --release --offline",
       "cp target/release/cleanroom-whisper {{ install_prefix }}/bin/"
   ]

Step 2: Local Testing (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test package creation on your local platform:

.. code:: bash

   # Create package for current platform
   airgap-deploy prep --output dist/cleanroom-whisper-local.tar.gz

   # Test in VM without network
   # 1. Transfer package to VM
   # 2. Extract and run install.sh
   # 3. Verify installation works

Step 3: Configure GitHub Actions for Multi-Platform Builds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``.github/workflows/release.yml``:

.. code:: yaml

   name: Release

   on:
     push:
       tags:
         - 'v*'

   jobs:
     build:
       name: Build for ${{ matrix.platform }}
       runs-on: ${{ matrix.os }}
       strategy:
         matrix:
           include:
             - os: ubuntu-latest
               platform: linux-x86_64
               artifact: cleanroom-whisper-linux-x86_64.tar.gz
             - os: macos-latest
               platform: macos-aarch64
               artifact: cleanroom-whisper-macos-aarch64.tar.gz
             - os: windows-latest
               platform: windows-x86_64
               artifact: cleanroom-whisper-windows-x86_64.zip

       steps:
         - uses: actions/checkout@v4

         - name: Install Rust
           uses: dtolnay/rust-toolchain@stable

         - name: Install AirGap Deploy
           run: cargo install airgap-deploy

         - name: Create air-gap package
           run: |
             airgap-deploy prep \
               --target ${{ matrix.platform }} \
               --output dist/${{ matrix.artifact }}

         - name: Upload artifact
           uses: actions/upload-artifact@v4
           with:
             name: ${{ matrix.artifact }}
             path: dist/${{ matrix.artifact }}

     release:
       name: Create Release
       needs: build
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - name: Download all artifacts
           uses: actions/download-artifact@v4
           with:
             path: dist/

         - name: Create Release
           uses: softprops/action-gh-release@v1
           with:
             files: dist/*/*.tar.gz
             body: |
               ## Air-Gapped Installation

               Download the package for your platform:
               - Linux (x86_64): `cleanroom-whisper-linux-x86_64.tar.gz`
               - macOS (Apple Silicon): `cleanroom-whisper-macos-aarch64.tar.gz`
               - Windows (x86_64): `cleanroom-whisper-windows-x86_64.zip`

               See installation instructions in the package README.txt

Step 4: Create Release
~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Tag new version
   git tag v0.1.0
   git push origin v0.1.0

   # GitHub Actions automatically:
   # 1. Builds packages on Linux, macOS, Windows runners
   # 2. Creates GitHub release
   # 3. Uploads packages as release assets

Step 5: Verify Release
~~~~~~~~~~~~~~~~~~~~~~

Go to GitHub Releases page
Verify all three platform packages are attached
Download and spot-check one package
Update release notes if needed

--------------

User Workflow: Installing on Air-Gapped System
----------------------------------------------

.. _prerequisites-1:

Prerequisites
~~~~~~~~~~~~~

- Air-gapped system (Linux, macOS, or Windows)
- USB drive or other transfer mechanism
- Basic build tools may be required:

  - Linux: C compiler (gcc), make, ALSA headers
  - macOS: Xcode Command Line Tools
  - Windows: Visual Studio Build Tools

Step 1: Download Package
~~~~~~~~~~~~~~~~~~~~~~~~

**On connected system:**

Go to https://github.com/yourusername/cleanroom-whisper/releases
Download package for target platform
Copy to USB drive

**Package sizes:**

- Linux: ~300 MB (includes Rust toolchain, whisper.cpp source, base.en model)
- macOS: ~350 MB
- Windows: ~400 MB

Step 2: Transfer to Air-Gapped System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Insert USB drive
   # Linux/macOS
   cp /media/usb/cleanroom-whisper-linux-x86_64.tar.gz ~/Downloads/

   # Windows
   copy E:\cleanroom-whisper-windows-x86_64.zip %USERPROFILE%\Downloads\

Step 3: Extract Package
~~~~~~~~~~~~~~~~~~~~~~~

**Linux/macOS:**

.. code:: bash

   cd ~/Downloads
   tar -xzf cleanroom-whisper-linux-x86_64.tar.gz
   cd cleanroom-whisper-linux-x86_64

**Windows:**

.. code:: powershell

   cd $env:USERPROFILE\Downloads
   Expand-Archive -Path cleanroom-whisper-windows-x86_64.zip -DestinationPath .
   cd cleanroom-whisper-windows-x86_64

Step 4: Review Package Contents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   ls -la

   # Expected contents:
   # cleanroom-whisper/         - Source code + vendored dependencies
   # whisper.cpp/            - whisper.cpp source code
   # models/                 - Whisper model files (base.en.bin)
   # rust-installer/         - Rust toolchain installer
   # install.sh              - Installation script (Linux/macOS)
   # install.ps1             - Installation script (Windows)
   # README.txt              - Installation instructions
   # airgap-deploy-metadata.json - Package metadata

Step 5: Run Installation Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Linux/macOS:**

.. code:: bash

   ./install.sh

**Windows:**

.. code:: powershell

   .\install.ps1

Step 6: Installation Process (Interactive Mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The install script will:

**Check dependencies:**

   ::

      === Cleanroom Whisper Installation ===

      Checking dependencies...
        ✓ Rust toolchain: Not found, will install
        ✓ C compiler (gcc): Found
        ✓ make: Found
        ✓ ALSA libraries: Found
        ✓ Disk space: 2.1 GB available (500 MB required)

      All dependencies satisfied.

**Prompt for installation location:**

   ::

      Where should Cleanroom Whisper be installed?
      [Default: ~/.local]:

   Press Enter for default, or specify custom path like ``/opt/cleanroom-whisper``

**Install Rust toolchain (if needed):**

   ::

      Installing Rust toolchain...
      This may take a few minutes...
      ✓ Rust installed to ~/.local

**Build whisper.cpp:**

   ::

      Building whisper.cpp...
      gcc -O3 -std=c11 ...
      ✓ whisper.cpp built successfully

**Build Cleanroom Whisper:**

   ::

      Building Cleanroom Whisper (offline mode)...
      Compiling cleanroom-whisper v0.1.0
      ✓ Cleanroom Whisper built successfully

**Install files:**

   ::

      Installing files...
        ~/.local/bin/whisper-main
        ~/.local/bin/cleanroom-whisper
        ~/.local/share/cleanroom-whisper/models/base.en.bin
        ~/.config/cleanroom-whisper/config.toml

      ✓ Installation complete!

**Summary:**

   ::

      === Installation Summary ===

      Cleanroom Whisper has been installed to: ~/.local/bin

      Configuration file: ~/.config/cleanroom-whisper/config.toml
      Model directory: ~/.local/share/cleanroom-whisper/models

      To run: cleanroom-whisper
      (Make sure ~/.local/bin is in your PATH)

      First run will prompt you to configure settings.

Step 7: First Run
~~~~~~~~~~~~~~~~~

.. code:: bash

   # Add to PATH if needed (Linux/macOS)
   export PATH="$HOME/.local/bin:$PATH"
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

   # Run Cleanroom Whisper
   cleanroom-whisper

**First-run experience:**

::

   === Cleanroom Whisper - First Run Setup ===

   Configuration file: ~/.config/cleanroom-whisper/config.toml

   Discovering whisper.cpp installation...
     Whisper path: ~/.local
     Binary found: ~/.local/bin/whisper-main ✓
     Models found:
       - base.en (140 MB) ✓
       - small.en (460 MB) ✓

   Settings look good! Starting Cleanroom Whisper...

   Tray icon should now appear in your system tray.

   Hotkeys:
     Ctrl+Alt+R - Toggle recording
     Ctrl+Alt+C - Copy last transcription

   Right-click tray icon for menu.

--------------

Alternative: Non-Interactive Installation
-----------------------------------------

For automated deployments (enterprise, CI/CD, etc.):

.. code:: bash

   # Linux/macOS
   MODE=automatic INSTALL_PREFIX=/opt/cleanroom-whisper ./install.sh

   # Windows
   $env:MODE="automatic"; $env:INSTALL_PREFIX="C:\Program Files\Cleanroom Whisper"; .\install.ps1

Non-interactive mode:

- Uses default settings
- No prompts
- Logs to ``install.log``
- Exits with code 0 on success, non-zero on failure

--------------

Troubleshooting
---------------

Installation fails: “C compiler not found”
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Linux:**

.. code:: bash

   # Debian/Ubuntu
   sudo apt install build-essential

   # Fedora/RHEL
   sudo dnf groupinstall "Development Tools"

   # Arch
   sudo pacman -S base-devel

**macOS:**

.. code:: bash

   xcode-select --install

**Windows:** Download and install Visual Studio Build Tools from the package if included, or download separately.

Installation fails: “ALSA not found” (Linux only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Debian/Ubuntu
   sudo apt install libasound2-dev libasound2

   # Fedora/RHEL
   sudo dnf install alsa-lib-devel alsa-lib

   # Arch
   sudo pacman -S alsa-lib

Or install from included packages (if SystemPackageComponent is in use):

.. code:: bash

   cd packages/debian
   sudo dpkg -i *.deb

“cleanroom-whisper: command not found”
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add installation directory to PATH:

.. code:: bash

   # Linux/macOS
   export PATH="$HOME/.local/bin:$PATH"
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

   # Windows
   # Add to PATH via System Properties > Environment Variables

Tray icon doesn’t appear (GNOME)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GNOME requires the AppIndicator extension:

.. code:: bash

   # Install extension
   gnome-extensions install appindicator@...

   # Or use browser:
   # https://extensions.gnome.org/extension/615/appindicator-support/

--------------

Package Size Estimates
----------------------

============== ================ =============== ==============
Platform       Components       Compressed Size Extracted Size
============== ================ =============== ==============
Linux x86_64   All              ~300 MB         ~800 MB
Linux x86_64   + small.en model ~700 MB         ~1.5 GB
macOS ARM      All              ~350 MB         ~900 MB
Windows x86_64 All              ~400 MB         ~1.0 GB
============== ================ =============== ==============

**Note:** Sizes include:

- Cleanroom Whisper source + vendored Rust dependencies (~100 MB)
- Rust toolchain installer (~150 MB compressed, ~500 MB extracted)
- whisper.cpp source (~10 MB)
- base.en model (~140 MB)

--------------

Version Update Workflow
-----------------------

When a new version of Cleanroom Whisper is released:

Developer Side
~~~~~~~~~~~~~~

Update version in ``Cargo.toml`` and ``AirGapDeploy.toml``
Update CHANGELOG.md
Create git tag: ``git tag v0.2.0``
Push tag: ``git push origin v0.2.0``
GitHub Actions creates new release automatically

User Side
~~~~~~~~~

Download new package from releases

Transfer to air-gapped system

Run installation script (will upgrade existing installation)

Install script detects existing installation:

   ::

      Existing installation found at ~/.local/bin

      Current version: 0.1.0
      New version: 0.2.0

      Upgrade? [Y/n]:

Backs up config and models

Installs new version

Restores config and models

--------------

Summary
-------

This workflow enables:

- **Developers:** Create multi-platform air-gap packages with single command
- **Users:** Install with single script, minimal interaction
- **Enterprises:** Automated deployment with non-interactive mode
- **Upgrades:** Smooth version updates preserving user data

The complete process from "create release" to "user running application" takes approximately:

- Developer: 5-10 minutes (mostly automated via CI/CD)
- User: 10-20 minutes (mostly building whisper.cpp and Cleanroom Whisper)
