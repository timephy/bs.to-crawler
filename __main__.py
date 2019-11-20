import bs_to
from host import vivo_sx
import requests
import time
import sys

from selenium import webdriver

SLEEP_TIME = 0.5
SUPPORTED_HOSTS = ["vivo"]

# season_url = input("The URL of the series: ")
assert len(sys.argv) > 1, "Error: No URL provided."
season_url = sys.argv[1]
season_url_parts = season_url.split("/")

assert len(season_url_parts) == 7
assert season_url_parts[0] == "http:" or season_url_parts[0] == "https:"
assert season_url_parts[1] == ""
assert season_url_parts[2] == "bs.to"
assert season_url_parts[3] == "serie"


def get_host_coverage(episodes):
    """Returns a dict mapping host_name to count."""
    coverage = {}  # dict(map(lambda host: (host, 0), all_host_names))
    for episode in episodes:
        for host in episode["hosts"]:
            if host[0] not in coverage:
                coverage[host[0]] = 0
            coverage[host[0]] += 1
    return coverage


def select_host_name(host_names):
    host_names = list(filter(lambda host: host in SUPPORTED_HOSTS, host_names))
    return host_names[0]  # for testing: auto-select first host
    while True:
        inp = input(f"> Select host ({host_names}): ")
        if inp in host_names:
            return inp
        else:
            print("Error: Selected host is not valid.")


def main(season_url):
    # Assert season url
    season_url = "/".join(season_url_parts[:7])
    base_url = "/".join(season_url_parts[:3])
    season_str = season_url_parts[5].zfill(2)

    # Get season data
    print(f"Requesting '{season_url}' to get data...")
    season_html = requests.get(season_url).text
    series_title = bs_to.get_series_title(season_html)
    episodes = bs_to.get_episodes(season_html)

    print(f"Title: {series_title}")
    print(f"Season: {season_str}")
    print(f"Episodes ({len(episodes)}):")
    for episode in episodes:
        hosts = list(map(lambda host: host[0], episode["hosts"]))
        episode_str = episode["id"].zfill(2)
        episode_title = episode["title"].ljust(40)
        print(f"""  {episode_str} {episode_title} ({hosts})""")
        # print(f"""       ({hosts})""")

    host_coverage = get_host_coverage(episodes)

    # Select Host
    time.sleep(SLEEP_TIME)
    print()
    print("Hosts:")
    for host_name, count in host_coverage.items():
        supported = " (supported)" if host_name in SUPPORTED_HOSTS else ""
        host_name = host_name.ljust(12)
        count = str(count).rjust(2)
        print(f"  {host_name} {count} / {len(episodes)}{supported}")
    # print()
    print(f"Currently Supported Hosts: {SUPPORTED_HOSTS}")
    print(f"(Please file an issue on GitHub about support for more hosts)")
    print()

    # Select host
    selected_host_name = select_host_name(host_coverage.keys())
    time.sleep(SLEEP_TIME)
    print(f"Selected host: {selected_host_name}")

    episodes_and_bs_urls_to_get = []
    for episode in episodes:
        hosts = dict(episode["hosts"])
        if selected_host_name in hosts:
            bs_url = hosts[selected_host_name]
            if bs_url is not None:
                episodes_and_bs_urls_to_get.append((episode, bs_url))

    # Browser
    """
    This options is essential, if not included bs.to recognizes it is
    controlled by automating code and won't link to the video.
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)

    # def interrupted(signum, stack):
    #     print("interrupted(signum, stack)")
    #     global RUN
    #     RUN = False
    #     # driver.quit()
    # signal.signal(signal.SIGINT, interrupted)

    outputs = []
    for episode, bs_url in episodes_and_bs_urls_to_get:
        time.sleep(SLEEP_TIME)
        episode_str = str(episode["id"]).zfill(2)
        episode_title = episode["title"]
        print()
        print(f"""# S{season_str}E{episode_str}: {episode_title} ({bs_url})""")

        # Get host url from bs.to
        host_url = bs_to.driver(driver, base_url + "/" + bs_url)
        print(f"→ {host_url=}")

        # Get video url from host
        video = vivo_sx.driver(driver, host_url)
        video_url = video["url"]
        print(f"→ {video_url=}")

        # File name
        quality_str = video["size"]
        file_format = video["type"].split("/")[1]
        file_name = f"{series_title} - S{season_str}E{episode_str} - {episode_title} - {quality_str}p.{file_format}"
        print(f"→ {file_name=}")

        outputs.append((file_name, video_url))

    # Data to file
    output_file_name = f"{series_title} - S{season_str}.csv"
    output_file = open(output_file_name, "w")
    output_file.write(", ".join(("file_name", "video_url")) + "\n")
    for output in outputs:
        output_file.write(", ".join(output) + "\n")
    output_file.close()

    # ffmpeg script to file
    ffmpeg_file_name = f"Download {series_title} - S{season_str}.sh"
    ffmpeg_file = open(ffmpeg_file_name, "w")
    video_output_dir = f"{series_title}/S{season_str}"
    ffmpeg_file.write(f"mkdir -p \"{video_output_dir}\"\n")
    for output in outputs:
        ffmpeg_file.write(
            f"ffmpeg -i {output[1]} \"{video_output_dir}/{output[0]}\"" + "\n")
    ffmpeg_file.close()

    print()
    print(f"→ Data file: {output_file_name}")
    print(f"→ Download script: {ffmpeg_file_name}")
    print("Done.")

    # raise Exception()


main(season_url)
