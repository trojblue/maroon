# maroon
Maroon is a package that manages music for Roon.

## Installation
install from PyPI:
```bash
pip install maroon
```

build from source:
```bash
git clone https://github.com/trojblue/maroon
cd maroon
poe install
poetry build
pip install dist/<build_version>.whl
```

## Usage
maroon rearranges your subfolders in an album dir into roon-friendly `DISC*/`format, and splits `.cue` files into individual`.flac` files, containing metadata: 
```bash
maroon <album dir>
```
