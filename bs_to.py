import requests
from bs4 import BeautifulSoup
import functools
import time
import os
import signal

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SITE_URL = "bs.to"
SUPPORTED_HOSTS = ["vivo"]

RUN = True

SLEEP_TIME = 1

# TYPES:
# season {"title": String, "id": String}
# episode {"id": String, "title": String, "hosts": [(name: String, url: String)]}
# video {"size": String, "format": String, "url": String}


def html_to_soup(func):
    @functools.wraps(func)
    def wrapper(html):
        soup = BeautifulSoup(html, "html.parser")
        return func(soup)
    return wrapper


def url_to_soup(func):
    @functools.wraps(func)
    def wrapper(url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        return func(soup)
    return wrapper


@url_to_soup
def get_season(soup):
    """Expects main series site."""
    serie = soup.find("section", {"class": "serie"})
    h2 = serie.h2
    title = list(h2.children)[0]
    id = h2.small.text
    return {"title": title.strip(), "id": id}


@url_to_soup
def get_episodes(soup):
    episodes = soup.find("table", {"class": "episodes"}).find_all("tr")

    def episode(tr):
        id = tr.find("a").text
        title = tr.find("strong").text
        hosts = list(tr.children)[5]
        hosts = hosts.find_all("a")
        hosts = list(map(lambda host:
                         (host["title"], host["href"]), hosts))

        # return (id, title, hosts)
        return {"id": id, "title": title, "hosts": hosts}

    return list(map(episode, episodes))


@html_to_soup
def get_host_url_from_html(soup):
    player = soup.find("div", {"class": "hoster-player"})
    a = player.find("a")
    return a["href"]


# @url_to_soup
# def vivo_get_video_url(soup):
#     # print(soup)
#     stream_content = soup.find("div", {"class": "stream-content"})
#     print(stream_content)
#     video = stream_content.find("video")
#     print(video)
#     return (video["src"], "type")

############################################################################


@html_to_soup
def vivo_get_video_html(soup):  # ".stream-content > div > button"
    # stream_content = soup.find("div", {"class": "stream-content"})
    # print(stream_content)
    source = soup.select_one(".stream-content > div > div > video > source")

    return {"size": source["size"], "type": source["type"], "url": source["src"]}

############################################################################


def select_host_name(host_names):
    print(host_names)
    host_names = list(filter(lambda host: host in SUPPORTED_HOSTS, host_names))
    return host_names[0]
    host_names = set(host_names)
    while True:
        inp = input(f"Select host ({host_names}): ")
        if inp in host_names:
            return inp
        else:
            print("Selected host is not valid.")


def check_url(season_url):
    series_url_parts = season_url.split("/")
    if series_url_parts[2] != SITE_URL:
        raise Exception("URL passed to wrong crawler")
    if series_url_parts[3] != "serie":
        raise Exception("URL path does not start with serie/")


############################################################################

def driver_bs_episode(driver, url):
    driver.get(url)

    # Click Play
    # once for ad-tab, once for play
    for i in range(2):
        driver.switch_to_window(driver.window_handles[-1])
        player = driver.find_element_by_class_name("hoster-player")
        player.click()

    # sleep until captcha is solved, if present
    wait = WebDriverWait(driver, 20)
    while RUN:
        try:
            print("Please solve the CAPTCHA in the browser if needed.")
            print("(You may reload the page.)")
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".hoster-player > a")))
            print("CAPTCHA completed.")
            return get_host_url_from_html(driver.page_source)
        except:
            pass


def driver_vivo(driver, url):
    # driver.get(host_url)
    # OR
    driver.switch_to_window(driver.window_handles[-1])

    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".stream-content > div > div > video > source")))
    return vivo_get_video_html(driver.page_source)

############################################################################


def main(season_url):
    # Assert season url
    season_url = "/".join(season_url.split("/")[:7])
    base_url = "/".join(season_url.split("/")[:3])
    print(f"Checking {season_url}...")
    check_url(season_url)

    # Get season data
    print(f"Requesting {season_url} to get data...")
    season = get_season(season_url)
    print(f"""Title: {season["title"]}""")
    print(f"""Season: {season["id"]}""")

    # Get episode data
    episodes = get_episodes(season_url)

    print(f"Episodes {len(episodes)}:")
    for episode in episodes:
        hosts = list(map(lambda host: host[0], episode["hosts"]))
        print(
            f""" {episode["id"].rjust(3)} - {episode["title"].ljust(40)}""")
        print(f"""       ({hosts})""")

    all_host_names = []
    for episode in episodes:
        for host in episode["hosts"]:
            all_host_names.append(host[0])
    all_host_names = list(set(all_host_names))  # remove duplicates

    host_coverage = dict(map(lambda host: (host, 0), all_host_names))
    for episode in episodes:
        for host in episode["hosts"]:
            host_coverage[host[0]] += 1

    # Select Host
    time.sleep(SLEEP_TIME)
    print()
    print("# Hosts:")
    for host_name, count in host_coverage.items():
        notes = "(supported)" if host_name in SUPPORTED_HOSTS else ""
        host_name = host_name.ljust(12)
        count = str(count).rjust(3)
        print(f"  {host_name} {count} / {len(episodes)} {notes}")
    print()
    print(f"  Currently Supported Hosts: {SUPPORTED_HOSTS}")
    print("  (Please file an issue on GitHub about support for more hosts.)")
    print()

    # Select host
    selected_host_name = select_host_name(all_host_names)
    time.sleep(SLEEP_TIME)
    print(f"Selected host: {selected_host_name}")

    episodes_and_bs_urls_to_get = []
    for episode in episodes:
        bs_url = dict(episode["hosts"])[selected_host_name]
        if bs_url is not None:
            episodes_and_bs_urls_to_get.append(
                (episode, bs_url))
            # (episode["id"], episode["title"], base_url + "/" + link))
    # print(episodes_and_bs_urls_to_get)

    # Browser
    options = webdriver.ChromeOptions()
    # this option is essential, if not included bs.to recognizes it is
    # controlled by automating code and won't link to the video
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)

    def interrupted(signum, stack):
        print("interrupted(signum, stack)")
        global RUN
        RUN = False
        # driver.quit()

    signal.signal(signal.SIGINT, interrupted)

    outputs = []
    for episode, bs_url in episodes_and_bs_urls_to_get:
        print()
        time.sleep(SLEEP_TIME)
        print(
            f"""# Episode {episode["id"]}: {episode["title"]} ({bs_url})""")

        # Get host url from bs.to
        host_url = driver_bs_episode(driver, base_url + "/" + bs_url)
        print(f"→ {host_url=}")

        # Get video url from host
        video = driver_vivo(driver, host_url)
        video_url = video["url"]
        print(f"→ {video_url=}")
        # (source["src"], source["type"], source["size"])

        season_str = "XX".zfill(2)
        episode_str = str(episode["id"]).zfill(2)
        quality_str = str(video["size"])
        file_format = video["type"].split("/")[1]
        file_name = f"""{season["title"]} - S{season_str}E{episode_str} - {episode["title"]} - {quality_str}p.{file_format}"""
        print(f"→ {file_name=}")

        outputs.append((file_name, video_url))

    # Write outputs to file
    output_file_name = f"""{season["title"]}.csv"""
    output_file = open(output_file_name, "w")
    for output in outputs:
        output_file.write(", ".join(output) + "\n")
    output_file.close()

    print()
    print(f"→ Output file: {output_file_name}")
    print("Done.")

    # raise Exception()
