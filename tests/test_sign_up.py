import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SignUpSeleniumTests(LiveServerTestCase):
    port = 8000

    def setUp(self):
        """Set up Selenium WebDriver."""
        self.browser = webdriver.Chrome()

    def tearDown(self):
        """Close the browser after tests."""
        self.browser.quit()

    def test_sign_up(self):
        """Test signing up a new user."""
        self.browser.get(f'{self.live_server_url}/api/signup/')
        username_input = self.browser.find_element(By.NAME, 'username')
        password1_input = self.browser.find_element(By.NAME, 'password1')
        password2_input = self.browser.find_element(By.NAME, 'password2')
        email_input = self.browser.find_element(By.NAME, 'email')
        name_input = self.browser.find_element(By.NAME, 'name')
        dob_input = self.browser.find_element(By.NAME, 'date_of_birth')

        self.new_username = "testnewuser"
        self.new_password = "newpassword123"
        username_input.send_keys(self.new_username)
        password1_input.send_keys(self.new_password)
        password2_input.send_keys(self.new_password)
        email_input.send_keys("testnewuser@example.com")
        name_input.send_keys("Test New User")
        dob_input.send_keys("2000-01-01")
        password2_input.send_keys(Keys.RETURN)
        time.sleep(0.2)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'profile-username'))
        )
        username_display = self.browser.find_element(By.CLASS_NAME, 'profile-username')
        self.assertEqual(username_display.text, ("@" + self.new_username))
