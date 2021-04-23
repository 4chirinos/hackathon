import os, re, sys, time, json, datetime, logging, configparser
from models import Profile
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from extractors import extract_name, extract_job_title, extract_location, extract_company, extract_contacts

loading_time = None
driver = None

def skip_remember_me():
    try:
        button_remember_me_not_now = driver.find_element_by_class_name('btn__secondary--large-muted')
        button_remember_me_not_now.click()
        time.sleep(loading_time)
    except:
        logging.info('No remember me page')

def skip_add_phone_number():
    try:
        button_add_phone_number_skip = driver.find_element_by_class_name('secondary-action')
        button_add_phone_number_skip.click()
        time.sleep(loading_time)
    except:
        logging.info('No add phone number page')

def login(config):
    driver.get('https://www.linkedin.com')
    input_username = driver.find_element_by_id('session_key')
    input_username.send_keys(config['username'])
    input_password = driver.find_element_by_id('session_password')
    input_password.send_keys(config['password'])
    button_log_in = driver.find_element_by_class_name('sign-in-form__submit-button')
    button_log_in.click()
    time.sleep(loading_time)

def get_urls(keywords):
    driver.get('https:www.google.com')
    time.sleep(loading_time)
    keywords = ' '.join(keywords)
    query = f'site:linkedin.com/in/ {keywords}'
    search_query = driver.find_element_by_name('q')
    search_query.send_keys(query)
    search_query.send_keys(Keys.ENTER)
    linkedin_results = driver.find_elements_by_class_name('yuRUbf')
    linkedin_urls = [anchor.get_attribute('href') for anchor in (linkedin_result.find_element_by_tag_name('a') for linkedin_result in linkedin_results)]
    linkedin_urls = list(map(lambda url: re.sub('^https://.+\.linkedin.com', 'https://www.linkedin.com', url), linkedin_urls))
    linkedin_urls = list(map(lambda url: re.sub('/..$|/..-..$', '', url), linkedin_urls))
    linkedin_urls = list(map(lambda url: url if url[len(url) - 1] != '/' else url[:len(url) - 1], linkedin_urls))
    return linkedin_urls

def get_contacts(url):
    url = url + '/detail/contact-info'
    logging.info('Calling: ' + url)
    driver.get(url)
    time.sleep(loading_time)
    html = BeautifulSoup(driver.page_source, 'html.parser')
    return extract_contacts(html)

def get_profile(url):
    logging.info('Calling: ' + url)
    driver.get(url)
    time.sleep(loading_time)
    html = BeautifulSoup(driver.page_source, 'html.parser')
    name = extract_name(html)
    job_title = extract_job_title(html)
    location = extract_location(html)
    company = extract_company(html)
    contacts = get_contacts(url)
    return Profile(name, job_title, location, company, contacts)

def to_json_file(profiles):
    project_folder_path = Path().absolute()
    current_time = str(datetime.datetime.now())
    file_location = f'{project_folder_path}/output/profiles_{current_time}.json'
    os.makedirs(os.path.dirname(file_location), exist_ok = True)
    with open(file_location, 'w', encoding = 'utf8') as f:
        json.dump(profiles, f, indent = 2, sort_keys = True, ensure_ascii = False)

def get_config(name):
    project_folder_path = Path().absolute()
    config = configparser.RawConfigParser()
    config.read(f'{project_folder_path}/config')
    return dict(config.items(name))

def launch_browser(config):
    global driver
    global loading_time
    loading_time = int(config['loading_time'])
    options = Options()
    options.headless = config['is_headless'] == 'True'
    driver = webdriver.Chrome('./chromedriver', options = options)

def main():
    handlers = [logging.FileHandler('hackathon.log'), logging.StreamHandler()]
    logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s', handlers = handlers, level = logging.INFO)
    logging.info('Started')
    launch_browser(get_config('SELENIUM'))
    login(get_config('LINKEDIN'))
    skip_remember_me()
    skip_add_phone_number()
    keywords = list(map(lambda arg: '"' + arg + '"', sys.argv[1:]))
    logging.info(f'Keywords: {keywords}')
    linkedin_urls = get_urls(keywords)
    profiles = list(map(lambda url: get_profile(url), linkedin_urls))
    to_json_file(profiles)
    logging.info('Finished')

if __name__ == '__main__':
    main()