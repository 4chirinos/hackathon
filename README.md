# Hackathon

## Overview

**Note**: Currently this only works with Chrome

Python project to retrieve basic details from linkedin profiles. It takes [this article](https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/) as reference

The flow is as follow:

1. It searches, in google, for linkedin profiles using the keywords it receives as arguments
2. It takes the results **ONLY** from the first page and proceeds to visit the linkedin profiles to pull the details
3. It saves the details in a csv file located in the "output" folder

## Requirements

- Python 3
- Pip 3
- The project was run using Chrome (Version 90.0.4430.85 (Official Build) (x86_64))

Probably you a different Chrome version. In that case, you will need to download the Selenium driver for that version.
Once you download the driver, remove the file "chromedriver" already present in the project
and paste the new one keeping the same name.

* **[You can download different driver versions from here](https://sites.google.com/a/chromium.org/chromedriver/downloads)**

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

## Issues

- It requires a linkedin accout, so it requires an email account too. Preferably a **GMAIL** account,
because it seems that the CCS style from linkedin page varies a little bit based on the type of the email account (not confirmed)

- From time to time, linkedin page show up modals or security checks because of the bot behavior
that the script has. In that case the script will fail. Try running again the script and hopefully
it will work. Otherwise, try setting a breakpoint in the section of code where the message appears
and solve it manually (human interaction). If it doesn't help, maybe the account is already banned (not confirmed)

- Eventually, in a matter of one day, linkedin blocks the account because it is detected as a bot.
Try not running too much tests, maybe it will help the account last longer (not confirmed)

## To be done

- Set up docker image, so we don't have to touch or install anything in our local environment. Currently, it requires
to have Chrome Version 90.0.4430.85
- Set up configuration to retrieve google results from the first N pages. Remember that right now
it is just retrieving the results from the first page
- Tune the filters and keyword definitions. At the moment it interprets each word as a seperated keyword.
For example: "python3 script.py k1 k2 k3" is interpreted as three keywords. Maybe we would like to
specify a keyword composed by two or more words, like "python3 script.py 'k1 k2' 'k3'"., where 'k1 k1'
is the first keyword and 'k3' the second one.
Besides, **don't forget it is using google search to find results**, so you can apply different filters
to narrow the scope. **Check**: https://support.google.com/websearch/answer/2466433?hl=en