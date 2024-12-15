from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogout:
    def test_logout(self, with_login):
        browser, username, password = with_login

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Log out']")))
        browser.find_element(By.XPATH, "//button[text()='Log out']").click()

        browser.get("http://localhost:5173/device-list")

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Увійти']")))
        assert browser.find_element(By.XPATH, "//h1[text()='Увійти']")
