# Hackathon

## Overview

Python project to retrieve basic details from linkedin profiles. It takes [this article](https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/) as reference

The flow is as follow:

1. It searches, in google, for linkedin profiles using the keywords it receives as arguments
2. It takes the results from google and proceeds to visit the linkedin profiles to pull the details
3. It saves the details in a csv file located in the "output" folder

## Requirements

- Python 3
- Pip 3
- The project was run using Chrome (Version 90.0.4430.85 (Official Build) (x86_64))

## Install dependencies

- Open terminal and run: pip3 install -r requirements

## Virtual environment (optional)

To avoid problems or version collisions with your local installation, you can use a virtual environment

You can run:
```sh
python3 -m venv hackathon
```

It will create a folder in the current location. Then run the next command:
```sh
source hackathon/bin/activate
```

If you want to deactivate it, just run:
```sh
deactivate
```

## Execute scraper

- It has to be run passing in the keywords as arguments: python3 main.py Nisum Chile