Use Case: SBOM/CBOM Generation During Deployment Packaging
==========================================================

Scenario
--------

A developer packages a Rust application for air-gapped deployment and needs a Software Bill of Materials (SBOM) and Cryptographic Bill of Materials (CBOM) for compliance, vulnerability management, and cryptographic inventory.

.. usecase:: SBOM/CBOM Generation During Deployment Packaging
   :id: UC-DEPLOY-003
   :status: proposed
   :tags: deploy, v1.1, sbom, cbom, workflow
   :priority: should
   :release: v1.1

   Generate a CycloneDX SBOM and CBOM during the ``prep`` phase, capturing the full dependency graph, license information, and cryptographic asset inventory. The SBOM is included in the deployment archive and travels with the software across the air gap.

   **Preparation:** Run ``airgap-deploy prep`` with ``--sbom`` flag. Deploy parses Cargo.lock, extracts dependency graph, detects cryptographic crates, and generates a unified CycloneDX document.

   **Transfer:** The SBOM file (``sbom.cdx.json``) is included in the deployment archive. AirGap Transfer verifies its integrity alongside all other files.

   **Air-gapped side:** The SBOM provides a complete inventory of deployed software, enabling offline vulnerability scanning (see :need:`UC-DEPLOY-004`) and cryptographic migration planning.

   **Success Criteria:** SBOM generated in valid CycloneDX JSON format, includes all transitive dependencies with versions and licenses, cryptographic crates identified and documented, file included in deployment archive.

--------------

Prerequisites
-------------

- **Connected machine:** Development machine with internet access
- **Rust project:** Application with ``Cargo.lock`` present (for dependency graph extraction)
- **AirGap Deploy v1.1:** Version with SBOM generation support

--------------

Workflow Steps
--------------

Phase 1: Preparation (Connected Machine)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create Deployment Manifest
^^^^^^^^^^^^^^^^^^^^^^^^^^

The deployment manifest is a standard ``AirGapDeploy.toml`` file. No additional configuration is required for SBOM generation — it is controlled via the CLI.

.. code:: toml

   # AirGapDeploy.toml
   [package]
   name = "secure-app"
   version = "1.0.0"
   description = "Internal application for air-gapped deployment"

   [[components]]
   type = "rust-app"
   name = "secure-app"
   path = "."

Generate Deployment Package with SBOM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   # Generate deployment package with SBOM/CBOM
   airgap-deploy prep --manifest AirGapDeploy.toml --sbom

   # Output:
   # - secure-app-v1.0.0.tar.gz (deployment archive)
   # - sbom.cdx.json (CycloneDX SBOM, also included in archive)

The ``--sbom`` flag triggers the following additional steps during ``prep``:

1. Parse ``Cargo.lock`` to extract the full transitive dependency graph
2. Read license fields from each dependency's ``Cargo.toml``
3. Scan the dependency list for known cryptographic crates
4. Document AirGap Deploy's own cryptographic usage (SHA-256 checksums)
5. Output a unified CycloneDX JSON document (SBOM + CBOM)

Review Generated SBOM
^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   # Inspect the SBOM (human-readable summary)
   cat sbom.cdx.json | python -m json.tool | head -50

   # Expected fields:
   # - bomFormat: "CycloneDX"
   # - specVersion: "1.6"
   # - components: [list of all dependencies]
   # - dependencies: [dependency graph relationships]
   # - compositions: [cryptographic asset entries]

--------------

Phase 2: Transfer
~~~~~~~~~~~~~~~~~

The SBOM is included in the deployment archive by default. When AirGap Transfer moves the archive across the air gap, the SBOM travels with it and is verified by the same SHA-256 integrity checks as every other file.

.. code:: bash

   # Transfer as normal — SBOM is inside the archive
   airgap-transfer pack secure-app-v1.0.0.tar.gz /media/usb-drive

--------------

Phase 3: Usage on Air-Gapped Side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the deployment archive is unpacked on the air-gapped system, the SBOM can be used for:

- **Vulnerability scanning:** Feed the SBOM into ``airgap-deploy scan`` with an offline vulnerability database (see :need:`UC-DEPLOY-004`)
- **Compliance auditing:** Review the component inventory and license data for regulatory compliance
- **Cryptographic migration planning:** Review the CBOM entries to identify components that will need updating when post-quantum algorithms are adopted

.. code:: bash

   # Extract the SBOM from the deployment archive
   tar -xzf secure-app-v1.0.0.tar.gz sbom.cdx.json

   # Scan for vulnerabilities (requires offline vuln DB)
   airgap-deploy scan --sbom sbom.cdx.json --db /path/to/grype-db

--------------

Success Criteria
----------------

- SBOM generated in valid CycloneDX JSON format (spec version 1.6)
- All transitive dependencies from ``Cargo.lock`` listed as components
- License information included for dependencies that declare it
- Known cryptographic crates identified and recorded as CBOM entries
- AirGap Deploy's own SHA-256 usage documented
- SBOM file included in deployment archive
- SBOM integrity verified after transfer across air gap

--------------

Error Scenarios
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Error
     - Cause
     - Recovery
   * - "Cargo.lock not found"
     - Rust project not built or lock file missing
     - Run ``cargo generate-lockfile`` before prep
   * - "Failed to parse Cargo.lock"
     - Corrupted or unsupported lock file format
     - Regenerate with ``cargo update``
   * - "License field missing"
     - Dependency lacks license metadata
     - Warning only -- component listed without license
   * - "SBOM validation failed"
     - Generated SBOM does not conform to schema
     - Report as bug -- CycloneDX schema validation

--------------

Related Requirements
--------------------

- :need:`FR-DEPLOY-073` — Generate CycloneDX SBOM
- :need:`FR-DEPLOY-074` — Parse Cargo.lock for Dependency Graph
- :need:`FR-DEPLOY-075` — Extract License Information
- :need:`FR-DEPLOY-076` — Include Component Metadata in SBOM
- :need:`FR-DEPLOY-077` — Include SBOM in Deployment Archive
- :need:`FR-DEPLOY-078` — Detect Cryptographic Dependencies
- :need:`FR-DEPLOY-079` — Document Internal Cryptographic Usage
- :need:`FR-DEPLOY-080` — Unified SBOM/CBOM Document

--------------

Related Documents
-----------------

- :doc:`AirGap Deploy Overview <overview>` — General deployment workflow
- :doc:`Ollama Deployment <use-case-ollama>` — Example deployment use case
- :doc:`Vulnerability Scanning <use-case-vulnerability-scanning>` — Offline scanning with generated SBOMs
- `Air-Gapping Your Software Supply Chain </blog/air-gapping-your-software-supply-chain>`_ — Blog post on supply chain security
