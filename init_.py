from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def init_driver(options=None):
    """
    Initialize and return a WebDriver instance.
    """
    if options is None:
        options = Options()  # Initialize options if not provided

    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # For Linux systems

    # Use Service class to integrate ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)  # Set page load timeout to 30 seconds
    return driver

def parse_html(html):
    """
    Parse HTML content with BeautifulSoup.
    """
    return BeautifulSoup(html, "html.parser")
