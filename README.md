# Hackathon

## Overview

Python project to retrieve basic details from linkedin profiles. It takes [this article](https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/) as reference

The flow is as follow:

1. It searches, in google, for linkedin profiles using the keywords it receives as arguments
2. It takes the results *ONLY* from the first page and proceeds to visit the linkedin profiles to pull the details
3. It saves the details in a csv file located in the "output" folder

## Requirements

- Python 3
- Pip 3
- The project was run using Chrome (Version 90.0.4430.85 (Official Build) (x86_64))

## Install dependencies

- Open terminal and run:
```sh
pip3 install -r requirements
```

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

Now you can run installation on this environment:
```sh
pip3 install -r requirements
```

If you want to deactivate it, just run:
```sh
deactivate
```

## Execute scraper

- It has to be run passing in the keywords as arguments. Examples below:
```sh
python3 script.py Nisum Chile
```
```sh
python3 script.py Nisum India Chief
```

## To be done

- Set up docker image, so we don't have to touch or install anything in our local environment
- Set up configuration to retrieve google results from the first N pages. Remember that right now
it is just retrieving the results from the first page
- Tune the filters and keyword definitions. At the moment it interprets each word as a seperated keyword.
For example: "python3 script.py k1 k2 k3" is interpreted as three keywords. Maybe we would like to
specify a keyword composed by two or more words, like "python3 script.py 'k1 k2' 'k3'"., where 'k1 k1'
is the first keyword and 'k3' the second one.