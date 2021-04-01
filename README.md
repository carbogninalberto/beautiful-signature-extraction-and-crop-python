# Beautiful Signature Extraction and Automatic Crop in Python

### Quick Intro

This is a simple script that uses **opencv** to make **signature** photos 
clearer and automatically **crop** the white space around it.

#### TODO

1. Implement automatic boxes cluster detection to extract multiple signatures.
2. Implement classifier to detect which clusters are a signature.

### Examples

Original signatures images:
![alt original](/original.jpg)

Signatures box:
![alt boxes](/result_boxes.jpg)

Signatures cropped:
![alt final](/results.jpg)

### Install

Install and configure the environment:

    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

Run the script for the images inside datataset

    python main.py
    