from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestProtected:
    def test_protected(self, with_login):
        browser, username, password = with_login

        browser.find_element(By.XPATH, "//a[@href='/device-list']").click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Мої девайси']")))
        assert browser.find_element(By.XPATH, "//h1[text()='Мої девайси']")

    def test_protected_without_login(self, browser):
        browser.get("http://localhost:5173/device-list")

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Увійти']")))
        assert browser.find_element(By.XPATH, "//h1[text()='Увійти']")
