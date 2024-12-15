import random
import string

from selenium.webdriver.common.by import By


class TestRegister():
    def test_register(self, browser):
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        email = f"{''.join(random.choices(string.ascii_letters + string.digits, k=8))}@gmail.com"
        password = "StrongPassword2024"

        browser.get("http://localhost:5173/")
        browser.find_element(By.XPATH, "//a[@href='/register']").click()

        username_field = browser.find_element(By.NAME, "username")
        username_field.click()
        username_field.send_keys(username)
        assert username_field.get_attribute("value") == username

        email_field = browser.find_element(By.NAME, "email")
        email_field.click()
        email_field.send_keys(email)
        assert email_field.get_attribute("value") == email

        password_field = browser.find_element(By.NAME, "password")
        password_field.click()
        password_field.send_keys(password)
        assert password_field.get_attribute("value") == password

        browser.find_element(By.XPATH, "//button[@type='submit']").click()

