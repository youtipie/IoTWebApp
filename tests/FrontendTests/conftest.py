import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="class")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def with_login(browser):
    email = "admin@gmail.com"
    password = "BobelaDen2005"

    browser.get("http://localhost:5173/")
    browser.find_element(By.XPATH, "//a[@href='/login']").click()

    email_field = browser.find_element(By.NAME, "email")
    email_field.click()
    email_field.send_keys(email)
    assert email_field.get_attribute("value") == email

    password_field = browser.find_element(By.NAME, "password")
    password_field.click()
    password_field.send_keys(password)
    assert password_field.get_attribute("value") == password

    browser.find_element(By.XPATH, "//button[@type='submit']").click()

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[text()='HomePage']")))

    return browser, email, password
