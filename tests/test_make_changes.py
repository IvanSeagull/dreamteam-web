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

    def test_make_changes_and_update_password(self):
        """Test logging in, making changes to the user profile, updating the password, and verifying the changes."""
        # Populate the database with users
        call_command('seed_db')
        User = get_user_model()
        seeded_user = User.objects.first()

        # Navigate to the login page
        self.browser.get(f'{self.live_server_url}/api/login/')

        # Find the username and password fields
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')
        username_input.send_keys(seeded_user.username)
        password_input.send_keys("testpassword")
        password_input.send_keys(Keys.RETURN)

        # Wait for the profile page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'profile-username'))
        )

        # Navigate to settings
        settings_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div[2]/button')
        settings_button.click()

        # Wait for the settings form to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'name'))
        )

        # Modify the name and email fields
        name_input = self.browser.find_element(By.ID, 'name')
        email_input = self.browser.find_element(By.ID, 'email')

        updated_name = seeded_user.name + "1"
        updated_email = "updated_" + seeded_user.email

        name_input.clear()
        name_input.send_keys(updated_name)
        email_input.clear()
        email_input.send_keys(updated_email)

        # Save changes
        save_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/form/button')
        save_button.click()

        # Navigate to hobbies settings
        hobbies_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/button[3]')
        hobbies_button.click()

        hobby_list = self.browser.find_element(By.CLASS_NAME, 'hobby-list')
        selected_hobbies = [hobby for hobby in hobby_list.find_elements(By.TAG_NAME, 'input') if hobby.is_selected()]

        # Select all hobbies
        hobby_list = self.browser.find_element(By.CLASS_NAME, 'hobby-list')
        selected_hobbies = [
            hobby for hobby in hobby_list.find_elements(By.CLASS_NAME, 'hobby-item')
            if 'selected' in hobby.get_attribute('class')
        ]

        # Select all hobbies
        for hobby in hobby_list.find_elements(By.CLASS_NAME, 'hobby-item'):
            if 'selected' not in hobby.get_attribute('class'):
                hobby.click()

        # Save changes
        save_hobbies_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/form/button')
        save_hobbies_button.click()

        # Navigate to security settings
        security_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/button[2]')
        security_button.click()

        # Wait for the password form to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'password1'))
        )

        # Update the password
        password1_input = self.browser.find_element(By.ID, 'password1')
        password2_input = self.browser.find_element(By.ID, 'password2')

        new_password = "123tgewdw"

        password1_input.send_keys(new_password)
        password2_input.send_keys(new_password)

        # Save the new password
        save_password_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/form/button')
        save_password_button.click()



        # Log out
        logout_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/nav/div/button')
        logout_button.click()

        # Navigate back to the login page
        self.browser.get(f'{self.live_server_url}/api/login/')

        # Wait for the login page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )

        # Log in with the new password
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')
        username_input.send_keys(seeded_user.username)
        password_input.send_keys(new_password)

        time.sleep(1)

        password_input.send_keys(Keys.RETURN)

        # Wait for the profile page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'profile-username'))
        )

        time.sleep(1)

        settings_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div[2]/button')
        settings_button.click()

        # Navigate to hobbies settings again
        hobbies_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/button[3]')
        hobbies_button.click()
        time.sleep(0.2)

        # Wait for the hobbies list to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'hobby-list'))
        )

        # Verify all hobbies are selected
        hobby_list = self.browser.find_element(By.CLASS_NAME, 'hobby-list')
        for hobby in hobby_list.find_elements(By.TAG_NAME, 'input'):
            self.assertTrue(hobby.is_selected())
