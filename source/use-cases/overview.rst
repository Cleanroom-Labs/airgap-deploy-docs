Use Case Analysis
=================

Purpose
-------

This document provides an overview of primary use cases for AirGap Deploy, a declarative packaging tool that enables developers to prepare any application for deployment on air-gapped systems using simple TOML manifests.

User Personas
-------------

Release Engineer
~~~~~~~~~~~~~~~~

- **Needs:** Automate packaging of applications for air-gapped customers
- **Environment:** CI/CD pipelines, GitHub Actions, multi-platform builds
- **Priority:** Reproducibility, automation, cross-platform support

Application Developer
~~~~~~~~~~~~~~~~~~~~~

- **Needs:** Package own application with complex dependencies for offline use
- **Environment:** Development machine with internet, targeting air-gapped systems
- **Priority:** Simple manifest format, handles Rust + native deps + ML models

IT Administrator
~~~~~~~~~~~~~~~~

- **Needs:** Deploy pre-built packages to air-gapped fleet
- **Environment:** Air-gapped workstations, enterprise infrastructure
- **Priority:** Unattended installation, predictable behavior, clear verification

Open-Source Maintainer
~~~~~~~~~~~~~~~~~~~~~~

- **Needs:** Offer air-gap-ready releases alongside standard releases
- **Environment:** GitHub releases, community users in restricted environments
- **Priority:** Low maintenance overhead, works for multiple platforms

Primary Use Cases
-----------------

+----------------------------------------------------------------------+-------------------------------+-----------------------------------------------+
| Use Case                                                             | Actor                         | Workflow                                      |
+======================================================================+===============================+===============================================+
| :doc:`Cleanroom Whisper Deployment <use-case-airgap-whisper>`        | Release engineer / developer  | Create manifest → prep → CI/CD → release      |
+----------------------------------------------------------------------+-------------------------------+-----------------------------------------------+
| :doc:`Ollama Deployment <use-case-ollama>`                           | IT administrator / developer  | Create manifest → prep → transfer → install   |
+----------------------------------------------------------------------+-------------------------------+-----------------------------------------------+

Common Requirements Across All Use Cases
-----------------------------------------

+--------------------------------------+-----------------------------------------------------------+
| Requirement                          | Rationale                                                 |
+======================================+===========================================================+
| Declarative manifests (TOML)         | Reproducible, version-controllable packaging              |
+--------------------------------------+-----------------------------------------------------------+
| Offline installation                 | Target systems have zero internet access                  |
+--------------------------------------+-----------------------------------------------------------+
| Checksum verification                | Ensure integrity of downloaded components                 |
+--------------------------------------+-----------------------------------------------------------+
| Cross-platform install scripts       | Bash (Linux/macOS) and PowerShell (Windows) generation    |
+--------------------------------------+-----------------------------------------------------------+
| Self-contained packages              | Single archive with all dependencies vendored             |
+--------------------------------------+-----------------------------------------------------------+

Integration Scenarios
---------------------

With AirGap Transfer
~~~~~~~~~~~~~~~~~~~~

When deployment packages exceed USB capacity, AirGap Transfer handles chunked transfer:

- Package created by AirGap Deploy is chunked by AirGap Transfer
- Chunks transferred across air-gap on multiple USB drives
- Reconstructed on target, then installed normally

**See:** :doc:`airgap-transfer:use-cases/overview`

With Cleanroom Whisper
~~~~~~~~~~~~~~~~~~~~~~

Cleanroom Whisper is AirGap Deploy's primary reference use case:

- AirGap Deploy packages Whisper binary, whisper.cpp source, and ML models
- Generated install script builds from source on the air-gapped system
- Post-install configuration enables auto-discovery of models and binary

**See:** :doc:`use-case-airgap-whisper`

With CI/CD Systems
~~~~~~~~~~~~~~~~~~

AirGap Deploy integrates with CI/CD for multi-platform releases:

- GitHub Actions matrix builds create platform-specific packages
- Release artifacts are uploaded automatically
- Users download pre-built packages from releases

Out of Scope
------------

The following are explicitly NOT supported:

+-----------------------------------+-------------------------------------------+
| Use Case                          | Why Not Supported                         |
+===================================+===========================================+
| Runtime application management    | AirGap Deploy is a packaging tool only    |
+-----------------------------------+-------------------------------------------+
| Container/Kubernetes deployment   | Targets desktop/server, not orchestrators |
+-----------------------------------+-------------------------------------------+
| Network-based deployment          | Violates air-gap design principle         |
+-----------------------------------+-------------------------------------------+
| Application-specific build logic  | Remains generic; apps define own steps    |
+-----------------------------------+-------------------------------------------+

Success Metrics
---------------

================================ =======================================
Metric                           Target
================================ =======================================
Package creation time            < 5 minutes (excluding downloads)
Installation success rate        > 95% on supported platforms
Manifest complexity              < 50 lines for typical application
Package integrity                100% checksum verification
Cross-platform support           Linux x86_64, macOS ARM, Windows x86_64
================================ =======================================

See Also
--------

- :doc:`Gap Analysis <gap-analysis>` - Detailed gap analysis for the Cleanroom Whisper deployment use case
- :doc:`Requirements (SRS) <../requirements/srs>` - Detailed functional requirements
- :doc:`Design (SDD) <../design/sdd>` - Architecture and implementation
- :doc:`Roadmap <../roadmap>` - Implementation roadmap
- :doc:`Principles </meta/principles>` - Design principles guiding all decisions
