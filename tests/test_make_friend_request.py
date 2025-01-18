import time

from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class SendSeleniumTest(LiveServerTestCase):
    port = 8000  # Explicitly set the test server port to 8000

    def setUp(self):
        """Set up Selenium WebDriver."""
        self.browser = webdriver.Chrome()

    def tearDown(self):
        """Close the browser after tests."""
        self.browser.quit()

    def test_send_friend_request(self):
        """Test logging in, navigating to the users page, sending a friend request, and verifying in the database."""
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

        # Find the first user card and send a friend request
        users_grid = self.browser.find_element(By.CLASS_NAME, 'users-grid')
        user_card = users_grid.find_element(By.CLASS_NAME, 'user-card')
        # user_card_area = user_card.find_element(By.TAG_NAME, 'a')
        user_card.click()
        time.sleep(0.5)
        friend_button = self.browser.find_element(By.CLASS_NAME, 'add-friend-button')
        receiver_username = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div[1]/div/p').text.strip()[1:]
        time.sleep(0.5)

        friend_button.click()

        # Verify the friend request button has changed state
        # self.assertIn('request-sent', friend_button.get_attribute('class'), "Friend request was not sent successfully.")

        # Verify in the database that a friend request was created
        from api.models import FriendRequest
        receiver = User.objects.get(username=receiver_username)
        friend_requests = FriendRequest.objects.filter(sender=test_user, receiver=receiver)
        time.sleep(1)
        self.assertTrue(friend_requests.exists(), "No friend request was created in the database for the correct receiver.")
