import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


LINKEDIN_EMAIL = os.environ.get("ENV_LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.environ.get("ENV_LINKEDIN_PASSWORD")
MY_PHONE = os.environ.get("ENV_MY_PHONE")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

DESIRED_URL = "https://www.linkedin.com/jobs/search/?currentJobId=3401718892&f_AL=true&f_E=2&geoId=102044150&keywords=python%20developer&location=British%20Columbia%2C%20Canada&refresh=true"

driver.get(DESIRED_URL)


sign_in_button = driver.find_element(By.LINK_TEXT, "Sign in")
sign_in_button.click()

#Wait for the next page to load.
time.sleep(5)

email_field = driver.find_element(By.ID, "username")
email_field.send_keys(LINKEDIN_EMAIL)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(LINKEDIN_PASSWORD)
password_field.send_keys(Keys.ENTER)

job_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

for listing in job_listings:
    print("called")
    listing.click()
    time.sleep(2)

    #Try to locate the apply button, if can't locate then skip the job.
    try:
        apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-s-apply button")
        apply_button.click()
        time.sleep(5)
        
        #If phone field is empty, then fill your phone number.
        phone = driver.find_element(By.CLASS_NAME, "fb-single-line-text__input")
        if phone.text == "":
            phone.send_keys(MY_PHONE)

        submit_button = driver.find_element(By.CSS_SELECTOR, "footer button")

        #If the submit_button is a "Next" button, then this is a multi-step application, so skip.
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
            close_button.click()
            time.sleep(2)
            discard_button = driver.find_elements(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")[1]
            discard_button.click()
            print("Complex application, skipped.")
            continue
        else:
            submit_button.click()
    
        #Once application completed, close the pop-up window.
        time.sleep(2)
        close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        close_button.click()

    #If already applied to job or job is no longer accepting applications, then skip.
    except NoSuchElementException:
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()

