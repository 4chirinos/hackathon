import logging
from models import Profile, Contact

NA = 'N/A'
FAILED = 'FAILED'

def extract_contacts(html):
    try:
        contact_sections = html.find_all('section', class_ = 'pv-contact-info__contact-type')
        contacts = list(map(_extract_contact, contact_sections))
        contacts = list(filter(lambda contact: contact != None, contacts))
        return contacts
    except Exception as e:
        logging.error(e)
        return list()

def extract_name(html):
    try:
        name = html.find('li', class_ = 'inline t-24 t-black t-normal break-words').text
        return name.strip() if name else NA
    except Exception as e:
        logging.error(e)
        return FAILED

def extract_job_title(html):
    try:
        job_title = html.find('h2', class_ = 'mt1 t-18 t-black t-normal break-words').text
        return job_title.strip() if job_title else NA
    except Exception as e:
        logging.error(e)
        return FAILED

def extract_location(html):
    try:
        location = html.find('li', class_ = 't-16 t-black t-normal inline-block').text
        return location.strip() if location else NA
    except Exception as e:
        logging.error(e)
        return FAILED

def extract_company(html):
    try:
        company = html.find('span', class_ = 'text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view').text
        return company.strip() if company else NA
    except Exception as e:
        logging.error(e)
        return FAILED

def _extract_contact(html):
    try:
        name = html.find('header', class_ = 'pv-contact-info__header').text.strip()
        value = html.find('a', class_ = 'pv-contact-info__contact-link').text.strip()
        return Contact(name, value)
    except Exception as e:
        logging.error(e)
        return None