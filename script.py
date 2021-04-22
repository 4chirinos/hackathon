import os, re, sys, csv, time, json, datetime, logging
from models import Profile
from pathlib import Path
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

email = 'hackathon63@gmail.com'
password = 'hackathon63'
loading_time = 4
NA = 'N/A'

options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver', options=options)

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

def login():
    driver.get('https://www.linkedin.com')
    input_username = driver.find_element_by_id('session_key')
    input_username.send_keys(email)
    input_password = driver.find_element_by_id('session_password')
    input_password.send_keys(password)
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
    return linkedin_urls

def get_contacts():
    try:
        button_contacts = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/div/div/main/div/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[3]/a')
        logging.info('Calling: ' + button_contacts.get_attribute('href'))
        button_contacts.click()
        time.sleep(loading_time)
        contact_details = driver.find_element_by_class_name('pv-profile-section').find_elements_by_tag_name('a')
        contacts = list(map(lambda detail: detail.get_attribute('href'), contact_details))
        return contacts
    except Exception as e:
        logging.error(e)
        return list()

def get_profile(url):
    url = re.sub('^https://.+\.linkedin.com', 'https://www.linkedin.com', url)
    logging.info('Calling: ' + url)
    driver.get(url)
    time.sleep(loading_time)
    selector = Selector(text=driver.page_source) 
    name = selector.xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/div/div/main/div/div[1]/section/div[2]/div[2]/div[1]/ul[1]/li/text()').extract_first()
    job_title = selector.xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/div/div/main/div/div[1]/section/div[2]/div[2]/div[1]/h2/text()').extract_first()
    location = selector.xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/div/div/main/div/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[1]/text()').extract_first()
    company = selector.xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/div/div/main/div/div[1]/section/div[2]/div[2]/div[2]/ul/li/a/span/text()').extract_first()
    name = name.strip() if name else NA
    job_title = job_title.strip() if job_title else NA
    location = location.strip() if location else NA
    company = company.strip() if company else NA
    contacts = get_contacts()
    profile = Profile(name, job_title, location, company, contacts)
    return profile

def to_csv(profiles):
    project_folder_path = Path().absolute()
    current_time = str(datetime.datetime.now())
    file_location = f'{project_folder_path}/output/profiles_{current_time}.csv'
    os.makedirs(os.path.dirname(file_location), exist_ok = True)
    csv_file = open(file_location, 'w')
    with csv_file:
        columns = ['Name', 'Job Title', 'Location', 'Company', 'Contacts']
        writer = csv.DictWriter(csv_file, fieldnames = columns)    
        writer.writeheader()
        for profile in profiles:
            writer.writerow({
                'Name': profile.name,
                'Job Title': profile.job_title,
                'Location': profile.location,
                'Company': profile.company,
                'Contacts': ';'.join(profile.contacts)
            })

def main():
    handlers = [logging.FileHandler('hackathon.log'), logging.StreamHandler()]
    logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s', handlers=handlers, level = logging.INFO)
    logging.info('Started')
    login()
    skip_remember_me()
    skip_add_phone_number()
    keywords = list(map(lambda arg: '"' + arg + '"', sys.argv[1:]))
    logging.info(f'Keywords: {keywords}')
    linkedin_urls = get_urls(keywords)
    profiles = list(map(lambda url: get_profile(url), linkedin_urls))
    to_csv(profiles)
    logging.info('Finished')

if __name__ == '__main__':
    main()