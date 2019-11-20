# bs.to-crawler
A web crawler that extracts video urls from [bs.to](https://bs.to) in bulk.


## Requirements

- python3.8 https://www.python.org/downloads/
- chromedriver https://chromedriver.chromium.org
- beautifulsoup4 `pip3.8 install beautifulsoup4`
- selenium `pip3.8 install selenium`
- requests `pip3.8 install requests`
- ffmpeg http://www.ffmpeg.org (only for downloading)


## Getting started

1. Visit [bs.to](https://bs.to) and select your desired series (including season and language). Copy the URL in the top bar of your browser (Should be of this form: `http://bs.to/serie/<series>/<season>/<language>`, e.g. `https://bs.to/serie/Downton-Abbey/1/en`).
2. Run the program in the command-line: `python3.8 . [URL]`
3. Get video links from the output file(s)!


## How it works

This tool uses selenium to parse and query html. It uses chromedriver to control a Chrome browser instance. This simulates a real user and browser. Conveniently this also allows *you* to solve the CAPTCHAs.


## Disclaimer

This tool does, at no point in time, store, stream or use copyrighted material - it only handles urls.

Use of this tool is at each users own risk. Under no circumstances shall the developer(s) be liable for and indirect, incidental, consequential, special or exemplary damages arising out of the services this tool provides.
