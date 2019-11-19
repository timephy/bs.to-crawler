# bs.to-crawler
A web crawler that extracts video urls from bs.to in bulk.

## Requirements

- python3.8 https://www.python.org/downloads/
- chromedriver https://chromedriver.chromium.org
- beautifulsoup4 `pip3.8 install beautifulsoup4`
- selenium `pip3.8 install selenium`

## Getting started

1. Visit https://bs.to and select your desired series (with season and language). Copy the URL in the top bar of your browser (Should be of this form: `http://bs.to/serie/<series>/<season>/<language>`).
2. Run the program in the command-line: `python3.8 main.py [URL]`
3. Get video links from the output file!

## Disclaimer

This tool is for a crawler which extracts video urls from http://bs.to. It does, at no point in time, store, stream or use copyrighted material - it only handles urls.

Use of this tool is at each users own risk. Under no circumstances shall the developer(s) be liable for and indirect, incidental, consequential, special or exemplary damages arising out of the services this tool provides.
