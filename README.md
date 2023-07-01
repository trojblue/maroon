# maroon
Maroon is a package that manages music for Roon.

[![Upload Python Package](https://github.com/trojblue/maroon/actions/workflows/python-publish.yml/badge.svg)](https://github.com/trojblue/maroon/actions/workflows/python-publish.yml)
[![PyPI version](https://badge.fury.io/py/maroon.svg)](https://badge.fury.io/py/maroon)
[![PyPI - License](https://img.shields.io/pypi/l/maroon)](https://www.gnu.org/licenses/gpl-3.0.en.html)
![Python](https://img.shields.io/badge/python-3.10-blue.svg) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation
install from PyPI:
```bash
pip install maroon
```

build from source:
```bash
git clone https://github.com/trojblue/maroon
cd maroon
poetry install
poetry build
pip install dist/<build_version>.whl
```

## Usage
maroon rearranges your subfolders in an album dir into roon-friendly `DISC*/`format, and splits `.cue` files into individual`.flac` files, containing metadata: 
```bash
maroon format <album dir>
```
