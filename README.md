
# Metadata Scrambler

A Python CLI tool to read, edit, delete, and scramble metadata from files (images, videos, audio, documents, and archives).

This tool helps you review your files’ metadata, allowing you to remove it, scramble it randomly while keeping the same size, or edit it manually. This is my first project, and the inspiration came from a quote by a former NSA chief:
> We kill people based on metadata.


**Important**:
This application bundles ExifTool as an archived dependency and uses it as a standalone executable.
Please be aware of the ExifTool version included, currently version 13.45.

## Installation

**Step 1**
Clone the repository
```bash
  git clone https://github.com/Green-Round-Circle/MetadataScrambler.git 
  cd MetadataScrambler
```
**Step 2**
Create a virtual enviroment and install requirements

For Windows:
```ps1
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
```
 If activation is blocked, run once:
```ps1
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

For Linux:
```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
```
**Step 3**
Run the application
## Usage/Examples

```bash
  python app.py InputFile -h
  usage: app.py [-h] InputFile [-r | -s | -sr | -d | -e | -x]

  positional arguments:
  InputFile         Input file

  options:
  -h, --help        show this help message and exit
  -r, --read        Read metadata
  -s, --scramble    Scramble metadata (same size)
  -sr, --rscramble  Scramble metadata (random size)
  -d, --delete      Delete metadata
  -e, --edit        Edit metadata
  -x, --exit        Exit program
```

