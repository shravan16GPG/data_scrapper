import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import time  # For additional delays if needed

# Define path to your .env file
env_file_path = "D:/my_project_starty/scraping_and_comparison/.env"

# Load environment variables from .env file
load_dotenv(dotenv_path=env_file_path)

# Fetch the username and password from environment variables
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Check if USERNAME and PASSWORD are loaded properly
print(f"Loaded USERNAME from .env: {USERNAME}")
print(f"Loaded PASSWORD from .env: {PASSWORD}")

if not USERNAME or not PASSWORD:
    raise ValueError("USERNAME or PASSWORD is not set in the .env file.")

def login_using_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to headless=True if needed
        page = browser.new_page()

        # Step 1: Open the website with an increased timeout
        try:
            print("Opening the website...")
            page.goto("https://starop05.com/", timeout=120000)  # Increased timeout to 120 seconds
            print("Website loaded successfully!")
        except Exception as e:
            print(f"Error loading the page: {e}")
            print(f"Current URL: {page.url}")  # Print the current URL to check if there's a redirect
            page.screenshot(path="error_screenshot.png")  # Capture the page on error
            browser.close()
            return

        # Step 2: Wait for the login button and click it
        try:
            print("Waiting for the login button to appear...")
            #Wait for the <a> tag with href="/login/login.php"
            login_button = page.wait_for_selector('a[href="/login/login.php"]', timeout=60000)
            if login_button:
                print("Login button found. Clicking it...")
                page.click('a[href="/login/login.php"]')  # Click the button
                print("Login button clicked successfully!")
            else:
                print("Login button not found or not visible.")
                browser.close()
                return
        except Exception as e:
            print(f"Error finding or clicking the login button: {e}")
            browser.close()
            return



        # Step 3: Wait for the login fields to load
        try:
            print("Waiting for login fields to appear...")
            page.wait_for_selector("#user_id", timeout=60000)
            print("Login fields loaded.")
        except Exception as e:
            print(f"Error waiting for login fields: {e}")
            browser.close()
            return

        # Step 4: Fill in login credentials
        print(f"Filling in username: {USERNAME} and password...")
        page.fill("#user_id", USERNAME)
        page.fill("#user_pw", PASSWORD)
        time.sleep(2)  # Simulate human delay
        
        # Step 5: Submit the login form
        try:
            print("Clicking the login button on the login form...")
            page.click(".login_btn")
        except Exception as e:
            print(f"Error clicking the login button: {e}")
            browser.close()
            return

        # Step 6: Wait for the page to load after login
        try:
            print("Waiting for the page to load after login...")
            page.wait_for_load_state("networkidle", timeout=60000)
            print("Page appears to have loaded.")
        except Exception as e:
            print(f"Error waiting for the page to load after login: {e}")
            browser.close()
            return

        # Step 7: Verify the login was successful
        current_url = page.url
        expected_url = "https://starop05.com/member/mypage_user_info.php"
        print(f"Current URL after login attempt: {current_url}")
        
        if current_url == expected_url:
            print(f"Login successful! Redirected to the expected URL: {current_url}")
            page.screenshot(path="dashboard_screenshot.png")
        else:
            print(f"Login failed or redirected to an unexpected URL: {current_url}")
            print("Page content after redirection:")
            #print(page.content())  # Print the page's HTML to debug issues
        
        # Close the browser
        browser.close()

if __name__ == "__main__":
    login_using_playwright()
