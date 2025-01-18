from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


class SendAndAcceptSeleniumTest(LiveServerTestCase):
    port = 8000  # Explicitly set the test server port to 8000

    def setUp(self):
        """Set up Selenium WebDriver."""
        self.browser = webdriver.Chrome()

    def tearDown(self):
        """Close the browser after tests."""
        self.browser.quit()

    def test_send_and_accept_friend_request(self):
        """Test sending a friend request, logging out, logging in as the receiver, and accepting the request."""
        # Populate the database with users
        call_command('seed_db')
        User = get_user_model()

        # Ensure the user has common hobbies with others
        users = User.objects.all()
        test_user = None
        for user in users:
            user_hobbies = set(user.hobbies.values_list('name', flat=True))
            for other_user in users.exclude(id=user.id):
                other_user_hobbies = set(other_user.hobbies.values_list('name', flat=True))
                if user_hobbies & other_user_hobbies:  # Check for at least one common hobby
                    test_user = user
                    break
            if test_user:
                break

        self.assertIsNotNone(test_user, "No user with common hobbies found. Regenerate the database.")

        # Navigate to the login page
        self.browser.get(f'{self.live_server_url}/api/login/')

        # Log in with the selected user's credentials
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')
        username_input.send_keys(test_user.username)
        password_input.send_keys("testpassword")
        password_input.send_keys(Keys.RETURN)
        time.sleep(0.2)

        # Wait for the profile page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'profile-username'))
        )

        # Navigate to the users page
        target_page_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/nav/div/div/a[1]')
        time.sleep(0.5)
        target_page_button.click()

        # Wait for the users page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'users-grid'))
        )

        # Find the receiver user card and send a friend request
        users_grid = self.browser.find_element(By.CLASS_NAME, 'users-grid')
        user_card = users_grid.find_element(By.CLASS_NAME, 'user-card')
        friend_button = user_card.find_element(By.CLASS_NAME, 'friend-button')
        receiver_username = user_card.find_element(By.TAG_NAME, 'p').text.strip()[1:]
        time.sleep(0.5)
        friend_button.click()

        # Fetch the receiver user from the database
        receiver_user = User.objects.get(username=receiver_username)

        # Log out
        logout_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/nav/div/button')
        time.sleep(0.5)
        logout_button.click()

        # Navigate back to the login page
        self.browser.get(f'{self.live_server_url}/api/login/')

        # Log in as the receiver user
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')
        username_input.send_keys(receiver_user.username)
        password_input.send_keys("testpassword")
        password_input.send_keys(Keys.RETURN)

        # Wait for the profile page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'profile-username'))
        )

        # Navigate to the first specified page
        first_page_link = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[3]/p/a')
        time.sleep(0.5)
        first_page_link.click()

        # Wait for the page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[1]/button[2]'))
        )

        # Navigate to the second specified page
        second_page_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/button[2]')
        time.sleep(0.5)
        second_page_button.click()

        # Wait for the list to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]'))
        )

        # Find and click the accept button
        accept_list = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]')
        accept_button = accept_list.find_element(By.CLASS_NAME, 'accept-button')
        time.sleep(0.5)
        accept_button.click()

        # Verify the friend request was accepted in the database
        from api.models import Friend
        time.sleep(0.5)
        print(Friend.objects.all())
        friends_record = Friend.objects.filter(first_user=test_user, second_user=receiver_user)
        self.assertTrue(friends_record.exists(), "The friendship was not created in the database.")
