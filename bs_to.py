from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# TYPES:
# episode {"id": String, "title": String, "hosts": [(name: String, url: String)]}
# video {"size": String, "format": String, "url": String}


def get_series_title(html):
    soup = BeautifulSoup(html, "html.parser")
    serie = soup.find("section", {"class": "serie"})
    h2 = serie.h2
    title = list(h2.children)[0].strip()
    return title


def get_episodes(html):
    soup = BeautifulSoup(html, "html.parser")

    episodes = soup.find("table", {"class": "episodes"}).find_all("tr")

    def episode(tr):
        id = tr.find("a").text
        title = tr.find("strong").text
        hosts = list(tr.children)[5]
        hosts = hosts.find_all("a")
        hosts = list(map(
            lambda host: (host["title"], host["href"]), hosts))

        return {
            "id": id,
            "title": title,
            "hosts": hosts
        }

    return list(map(episode, episodes))


def get_host_url(html):
    soup = BeautifulSoup(html, "html.parser")
    player = soup.find("div", {"class": "hoster-player"})
    a = player.find("a")
    return a["href"]

############################################################################


def driver(driver, url):
    driver.get(url)

    # Click Play
    # once for ad-tab, once for play
    for i in range(2):
        driver.switch_to_window(driver.window_handles[-1])
        player = driver.find_element_by_class_name("hoster-player")
        player.click()

    # Solve CAPTCHA, if present
    wait = WebDriverWait(driver, 20)
    while True:
        try:
            print("Please solve the CAPTCHA in the browser if needed.")
            print("(You may reload the page)")
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".hoster-player > a")))
            print("CAPTCHA completed.")
            break  # break out of loop
        except:
            pass

    return get_host_url(driver.page_source)
