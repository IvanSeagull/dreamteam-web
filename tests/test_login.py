import time

from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class LoginSeleniumTests(LiveServerTestCase):
    port = 8000  # Explicitly set the test server port to 8000

    def setUp(self):
        """Set up Selenium WebDriver."""
        self.browser = webdriver.Chrome()

    def tearDown(self):
        """Close the browser after tests."""
        self.browser.quit()

    def test_login(self):
        """Test logging in with a seeded user."""
        # Populate the database with users
        call_command('seed_db')
        User = get_user_model()
        seeded_user = User.objects.first()

        # Navigate to the login page
        self.browser.get(f'{self.live_server_url}/api/login/')

        # Find the username and password fields
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')

        # Log in with a seeded user
        username_input.send_keys(seeded_user.username)
        password_input.send_keys("testpassword")
        password_input.send_keys(Keys.RETURN)
        time.sleep(0.5)

        # Verify the username is displayed correctly after login
        username_display = self.browser.find_element(By.CLASS_NAME, 'profile-username')
        self.assertEqual(username_display.text, ("@" + seeded_user.username))
