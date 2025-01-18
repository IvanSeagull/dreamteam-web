import time

from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class TestCommonHobbies(LiveServerTestCase):
    port = 8000  # Explicitly set the test server port to 8000

    def setUp(self):
        """Set up Selenium WebDriver."""
        self.browser = webdriver.Chrome()

    def tearDown(self):
        """Close the browser after tests."""
        self.browser.quit()

    def test_user_with_common_hobbies_and_age_filter(self):
        """Test selecting a user with common hobbies, applying an age filter, and verifying the results."""
        # Populate the database with users
        call_command('seed_db')
        User = get_user_model()

        # Fetch a user who has at least one common hobby with others
        users = User.objects.all()
        common_hobby_user = None
        for user in users:
            user_hobbies = set(user.hobbies.values_list('name', flat=True))
            for other_user in users.exclude(id=user.id):
                other_user_hobbies = set(other_user.hobbies.values_list('name', flat=True))
                if user_hobbies & other_user_hobbies:  # Check for at least one common hobby
                    common_hobby_user = user
                    break
            if common_hobby_user:
                break

        # If no user with at least one common hobby is found, skip further checks
        if common_hobby_user is None:
            return
        common_hobbies = set(common_hobby_user.hobbies.values_list('name', flat=True))

        # Navigate to the login page
        self.browser.get(f'{self.live_server_url}/api/login/')

        # Log in with the selected user's credentials
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')
        username_input.send_keys(common_hobby_user.username)
        password_input.send_keys("testpassword")
        password_input.send_keys(Keys.RETURN)

        # Wait for the profile page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'profile-username'))
        )

        # Navigate to the users page
        target_page_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/nav/div/div/a[1]')
        target_page_button.click()

        # Wait for the users page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'users-grid'))
        )

        # Input max age filter
        max_age_input = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div/label[2]/input')
        max_age = 30
        max_age_input.clear()
        max_age_input.send_keys(str(max_age))
        max_age_input.send_keys(Keys.RETURN)
        time.sleep(0.2)

        # Wait for the users grid to update
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'users-grid'))
        )

        # Verify users in the grid
        users_grid = self.browser.find_element(By.CLASS_NAME, 'users-grid')
        user_cards = users_grid.find_elements(By.CLASS_NAME, 'user-card')

        for user_card in user_cards:
            # Verify age is less than or equal to max age
            age_text = user_card.find_element(By.XPATH, './/p[contains(text(), "Age")]').text
            age = int(age_text.split(":")[1].strip())
            self.assertLessEqual(age, max_age, f"User age {age} exceeds max age {max_age}.")

            # Verify common hobbies are displayed
            common_hobbies_text = user_card.find_element(By.XPATH, './/p[contains(text(), "Common Hobbies")]').text
            common_hobbies_count = int(common_hobbies_text.split("(")[1].split(")")[0])
            self.assertGreater(common_hobbies_count, 0, "User does not have common hobbies.")

            # Verify at least one of the common hobbies is correct
            displayed_hobbies = [
                hobby.strip() for hobby in user_card.find_element(By.CLASS_NAME, 'hobby-tags').text.replace('\n', ',').split(',')
            ]
            time.sleep(0.2)

            self.assertTrue(
                any(hobby in common_hobbies for hobby in displayed_hobbies),
                f"Displayed hobbies {displayed_hobbies} do not include any common hobbies {common_hobbies}."
            )
