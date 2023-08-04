# maroon
Maroon is a package that manages music for Roon.

[![Upload Python Package](https://github.com/trojblue/maroon/actions/workflows/python-publish.yml/badge.svg)](https://github.com/trojblue/maroon/actions/workflows/python-publish.yml)
[![PyPI version](https://badge.fury.io/py/maroon.svg)](https://badge.fury.io/py/maroon)
[![PyPI - License](https://img.shields.io/pypi/l/maroon)](https://www.gnu.org/licenses/gpl-3.0.en.html)
![Python](https://img.shields.io/badge/python-3.10-blue.svg) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Features
convert `wav` and `cue` files into flac tracks, 
- split tracks into folders according to disc number
- adding genre info into metadata
```bash
maroon format <something.cue>
```
sample run:
```bash
Name of the album (default: i): 菊花夜行军
Genre of the album (split by ; sign):Chinese; Folk; Acoustic; Chinese Folk; Avant Folk; Folk Rock
Splitting CDImage: 100%|██████████| 10/10 [00:07<00:00,  1.37it/s]
Split 10 tracks.
```


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
