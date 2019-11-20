from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def _get_video(html):  # ".stream-content > div > button"
    """Returns the video url linked in the html (of vivo.sx)."""
    soup = BeautifulSoup(html, "html.parser")

    source = soup.select_one(".stream-content > div > div > video > source")
    return {
        "size": source["size"],
        "type": source["type"],
        "url": source["src"]
    }


def driver(driver, url):
    """All driver actions to perform."""
    # driver.get(host_url)
    # OR
    driver.switch_to_window(driver.window_handles[-1])

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".stream-content > div > div > video > source")))
    return _get_video(driver.page_source)
