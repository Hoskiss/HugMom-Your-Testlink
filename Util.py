from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element(browser, by, value, timeout=20):
    """
    wait for element to present in the browser
    """
    wait = WebDriverWait(browser, timeout)
    wait.until(EC.presence_of_element_located((by, value)))
    return browser.find_element(by, value)