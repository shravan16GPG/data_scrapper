from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Define path to your .env file
env_file_path = "D:/my_project_starty/scraping_and_comparison/.env"

# Load environment variables from .env file
load_dotenv(dotenv_path=env_file_path)

# Fetch the username and password from environment variables
USERNAME = "ysk7774"
PASSWORD = "opop0opop0"

def login_using_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
        page = browser.new_page()

        try:
            # Step 1: Open the login page
            print("Opening the login page...")
            page.goto("https://starop05.com/login/login.php", timeout=120000)
            print("Login page loaded successfully!")
        except Exception as e:
            print(f"Error loading the login page: {e}")
            browser.close()
            return

        try:
            # Step 2: Locate the input fields by their type and enter credentials
            print(f"Filling in username: {USERNAME} and password...")
            username_input = page.wait_for_selector('input[type="text"]#user_id', timeout=60000)
            password_input = page.wait_for_selector('input[type="password"]#user_pw', timeout=60000)

            # Fill in the username and password
            username_input.fill(USERNAME)
            password_input.fill(PASSWORD)
            print("Credentials entered successfully!")
        except Exception as e:
            print(f"Error finding or filling login fields: {e}")
            browser.close()
            return

        try:
            # Step 3: Click the login button
            print("Clicking the login button...")
            login_button = page.wait_for_selector('a.login_btn', timeout=60000)
            login_button.click()
            print("Login button clicked successfully!")
        except Exception as e:
            print(f"Error clicking the login button: {e}")
            browser.close()
            return

        try:
            # Step 4: Wait for the page to load after login
            print("Waiting for the page to load after login...")
            page.wait_for_load_state("networkidle", timeout=60000)
            print("Page appears to have loaded.")
        except Exception as e:
            print(f"Error waiting for the page to load after login: {e}")
            browser.close()
            return

        # # Step 5: Verify the login was successful
        # current_url = page.url
        # expected_url = "https://starop05.com/member/mypage_user_info.php"
        # print(f"Current URL after login attempt: {current_url}")
        
        # if current_url == expected_url:
        #     print(f"Login successful! Redirected to the expected URL: {current_url}")
        #     page.screenshot(path="dashboard_screenshot.png")
        # else:
        #     print(f"Login failed or redirected to an unexpected URL: {current_url}")
        
        # # Close the browser
        # browser.close()

if __name__ == "__main__":
    login_using_playwright()
