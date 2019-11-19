import bs_to
import urllib3.exceptions

# input("The URL of the series: ")
series_url = "https://bs.to/serie/Rick-and-Morty/1/de#44i8qoc4c"

if not (series_url.startswith("http://") or series_url.startswith("https://")):
    raise Exception("Series URL does not start with http:// or https://")

site = series_url.split("/")[2]

sites = {
    "bs.to": bs_to
}

if site not in sites:
    raise Exception(f"Series URL ({site}) is not supported.")

print(f"# Recognized site: {site}")

try:
    sites[site].main(series_url)
# except urllib3.exceptions.HTTPError as e:
#     pass
except Exception as e:
    raise e
