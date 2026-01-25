Workflow: Ollama Deployment to Air-Gapped System
================================================

Scenario
--------

Deploy Ollama (LLM runtime) and models to an air-gapped production system for local AI inference without internet connectivity.

.. usecase:: Ollama Deployment to Air-Gapped System
   :id: UC-DEPLOY-002
   :status: approved
   :tags: deploy, workflow, ollama, llm

   Deploy Ollama runtime and LLM models to air-gapped production system for local AI inference without internet connectivity.

   **Preparation:** Download Ollama binary and models (3-20GB), create deployment package with installation scripts.

   **Transfer:** Move package via USB or chunked transfer for large models.

   **Installation:** Extract package, run installation script to install binary, models, and systemd service.

   **Success Criteria:** Ollama runs as service, models load successfully, inference works offline, no network calls attempted.

--------------

Prerequisites
-------------

- **Connected machine:** Development machine with internet access
- **Air-gapped machine:** Production system with no network
- **Transfer method:** USB drives or airgap-transfer utility
- **Target:** Ollama binary + one or more LLM models

--------------

Workflow Steps
--------------

Phase 1: Preparation (Connected Machine)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create Deployment Manifest
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: toml

   # AirGapDeploy.ollama.toml

   [package]
   name = "ollama-deploy"
   version = "0.15.0"
   description = "Ollama runtime with llama2 model for air-gapped deployment"

   [install]
   prefix = "/opt/ollama"
   user = "ollama"
   group = "ollama"

   # Ollama binary
   [[components]]
   type = "external-binary"
   name = "ollama"
   source.type = "github-release"
   source.repo = "ollama/ollama"
   source.tag = "v0.15.0"
   source.asset_pattern = "ollama-linux-amd64"
   install_path = "bin/ollama"

   # Llama2 model (7B variant)
   [[components]]
   type = "model-file"
   name = "llama2-7b"
   source.type = "url"
   source.url = "https://ollama.ai/download/llama2-7b.gguf"
   source.checksum = "sha256:abc123..."
   install_path = "models/llama2-7b.gguf"

   # Optional: Mistral model
   [[components]]
   type = "model-file"
   name = "mistral-7b"
   source.type = "url"
   source.url = "https://ollama.ai/download/mistral-7b.gguf"
   source.checksum = "sha256:def456..."
   install_path = "models/mistral-7b.gguf"
   required = false  # Only included if specified

   # Systemd service file (Linux)
   [[components]]
   type = "config-file"
   name = "ollama.service"
   content = """
   [Unit]
   Description=Ollama LLM Server
   After=network.target

   [Service]
   Type=simple
   User=ollama
   WorkingDirectory=/opt/ollama
   ExecStart=/opt/ollama/bin/ollama serve
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   """
   install_path = "/etc/systemd/system/ollama.service"

Prepare Deployment Package
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   # On connected machine
   airgap-deploy prep --manifest AirGapDeploy.ollama.toml

   # Downloads:
   # - ollama binary (~100MB)
   # - llama2 model (~3.8GB)
   # - Generates installation scripts

   # Output: ollama-deploy-v0.15.0.tar.gz (~4GB)

Transfer Package
^^^^^^^^^^^^^^^^

**Option A: Single USB (if package fits)**

.. code:: bash

   cp ollama-deploy-v0.15.0.tar.gz /media/usb-drive/

**Option B: Chunked Transfer (for large models)**

.. code:: bash

   # Use airgap-transfer for packages > USB capacity
   airgap-transfer pack ollama-deploy-v0.15.0.tar.gz /media/usb-drive

--------------

Phase 2: Physical Transfer
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Physically move USB drive(s) across air-gap boundary
- Maintain chain of custody if required for security compliance

--------------

Phase 3: Installation (Air-Gapped Machine)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract Package
^^^^^^^^^^^^^^^

.. code:: bash

   # On air-gapped machine
   tar -xzf /media/usb/ollama-deploy-v0.15.0.tar.gz
   cd ollama-deploy-v0.15.0

Review Installation Plan
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   ./install.sh --dry-run

   # Shows:
   # - Where files will be installed
   # - What system changes will be made
   # - Required permissions

Execute Installation
^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   sudo ./install.sh

   # Installation steps:
   # 1. Create ollama user and group
   # 2. Create /opt/ollama directory structure
   # 3. Copy ollama binary to /opt/ollama/bin/
   # 4. Copy models to /opt/ollama/models/
   # 5. Set file permissions and ownership
   # 6. Install systemd service file
   # 7. Reload systemd daemon

Verify Installation
^^^^^^^^^^^^^^^^^^^

.. code:: bash

   # Check binary installation
   /opt/ollama/bin/ollama --version
   # Expected: Ollama version 0.15.0

   # Check models
   ls -lh /opt/ollama/models/
   # Expected: llama2-7b.gguf (~3.8GB)

   # Check systemd service
   sudo systemctl status ollama
   # Expected: inactive (dead) - not started yet

Start Ollama Service
^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   # Start service
   sudo systemctl start ollama

   # Enable on boot
   sudo systemctl enable ollama

   # Verify running
   sudo systemctl status ollama
   # Expected: active (running)

Test Inference
^^^^^^^^^^^^^^

.. code:: bash

   # Test llama2 model
   /opt/ollama/bin/ollama run llama2-7b "Hello, how are you?"

   # Expected: Model loads, generates response

--------------

Success Criteria
----------------

- ✅ Ollama binary installed and executable
- ✅ All specified models present and loadable
- ✅ Service starts automatically on boot
- ✅ Inference works correctly with offline models
- ✅ No network calls attempted during operation
- ✅ Installation repeatable and documented

--------------

Variations
----------

Multiple Models Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Create deployment with multiple models
   airgap-deploy prep --manifest AirGapDeploy.ollama.toml \
     --include mistral-7b \
     --include codellama-7b

   # Result: ~12GB package with 3 models

Update Existing Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Deploy new model to existing Ollama installation
   airgap-deploy prep --manifest AirGapDeploy.ollama-update.toml

   # Manifest contains only new model
   # Installation script detects existing Ollama, adds model

--------------

Error Scenarios
---------------

+---------------------------+----------------------------------+----------------------------------------------+
| Error                     | Cause                            | Recovery                                     |
+===========================+==================================+==============================================+
| “Binary not found”        | Wrong asset pattern for platform | Update manifest with correct pattern         |
+---------------------------+----------------------------------+----------------------------------------------+
| “Model checksum mismatch” | Corrupted download               | Re-download model, update checksum           |
+---------------------------+----------------------------------+----------------------------------------------+
| “Permission denied”       | Insufficient privileges          | Run install.sh with sudo                     |
+---------------------------+----------------------------------+----------------------------------------------+
| “Service failed to start” | Binary incompatible with system  | Check platform compatibility (x86_64 vs ARM) |
+---------------------------+----------------------------------+----------------------------------------------+
| “Out of disk space”       | Insufficient space for models    | Free disk space or deploy smaller models     |
+---------------------------+----------------------------------+----------------------------------------------+

--------------

Integration Points
------------------

With airgap-transfer
~~~~~~~~~~~~~~~~~~~~

For large deployments (multiple models > USB capacity, see :doc:`airgap-transfer workflows </airgap-transfer/use-cases/overview>`):

.. code:: bash

   # 1. Prepare deployment package
   airgap-deploy prep --manifest AirGapDeploy.ollama-full.toml
   # Output: ollama-deploy-full.tar.gz (20GB with all models)

   # 2. Use airgap-transfer to chunk
   airgap-transfer pack ollama-deploy-full.tar.gz /media/usb-drive --chunk-size 16GB

   # 3. Transfer chunks across air-gap

   # 4. Reconstruct on air-gapped machine
   airgap-transfer unpack /media/usb-drives ~/deployment/

   # 5. Install as normal
   cd ~/deployment/ollama-deploy-full
   sudo ./install.sh

With Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For large-scale deployments:

.. code:: bash

   # Generate Ansible playbook from manifest
   airgap-deploy prep --manifest AirGapDeploy.ollama.toml --format ansible

   # Output: ansible/ollama-deploy.yml
   # Can be integrated with existing configuration management

--------------

Security Considerations
-----------------------

==================== ================================================
Concern              Mitigation
==================== ================================================
Binary authenticity  Verify checksums against official releases
Model provenance     Download from official Ollama registry only
Privilege escalation Install script requires explicit sudo
File permissions     Ollama runs as dedicated user, not root
Network isolation    Verify no network calls with firewall monitoring
==================== ================================================

--------------

Post-Deployment Verification
----------------------------

.. code:: bash

   # 1. Verify no network calls
   sudo iptables -L | grep ollama  # Should show no rules
   sudo lsof -i -a -p $(pgrep ollama)  # Should show no connections

   # 2. Verify model functionality
   /opt/ollama/bin/ollama run llama2-7b "Explain quantum computing"

   # 3. Verify service persistence
   sudo reboot
   # After reboot:
   sudo systemctl status ollama  # Should be active (running)

   # 4. Performance baseline
   time /opt/ollama/bin/ollama run llama2-7b "Hello"
   # Record inference time for future comparison

--------------

Related Documents
-----------------

- :doc:`airgap-deploy Overview <overview>` - General deployment workflow and gap analysis
- :doc:`airgap-transfer </airgap-transfer/use-cases/overview>` - Large file transfer use cases
- :doc:`Cleanroom Whisper Workflow <workflow-airgap-whisper>` - Similar deployment workflow
- :doc:`Principles </meta/principles>` - Design principles for all AirGap tools
