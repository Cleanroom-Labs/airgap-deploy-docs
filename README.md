# AirGap Deploy Documentation

Documentation for AirGap Deploy - a universal Rust tool for preparing software deployments for air-gapped systems.

## Building Documentation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build HTML documentation
make html

# Open in browser
open build/html/index.html
```

## Project Structure

```
airgap-deploy-docs/
├── source/
│   ├── index.rst              # Main documentation entry
│   ├── conf.py                # Sphinx configuration (imports shared theme)
│   ├── readme.rst             # Project overview
│   ├── roadmap.md             # Implementation roadmap
│   ├── requirements/          # Software requirements
│   ├── design/                # Design documents
│   ├── testing/               # Test plans
│   ├── use-cases/             # Use case documentation
│   └── api/                   # API documentation
├── requirements.txt           # Python dependencies
├── Makefile                   # Build commands
└── README.md                  # This file
```

## Shared Theme

This documentation imports the shared Cleanroom Labs theme from the nested submodule at `source/cleanroom-theme/`.

## Cross-Project References

To reference other AirGap projects:
- `:doc:`airgap-whisper:installation``
- `:doc:`airgap-transfer:usage``

## Resources

- [AirGap Deploy Overview](source/readme.rst)
- [Requirements Specification](source/requirements/srs.rst)
- [Design Document](source/design/sdd.rst)
- [Roadmap](source/roadmap.md)
