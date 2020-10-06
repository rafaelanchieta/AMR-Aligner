# Semantically Inspired AMR Alignment for the Portuguese Language

This repository contains the source code for the BR-Aligner

## Requirements
- Python (3 or later)
- `pip install -r requirements.txt`
- `python3 config/config.py` to download the pre-trained models for Portuguese
- `sh download.sh` to download the pre-trained embeddings

## Usage
`python aligner.py -f input.txt`
- The results will be in the `output` folder
