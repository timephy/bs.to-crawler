# bs.to-crawler
A web crawler that extracts video urls from [bs.to](https://bs.to) in bulk.

## Attention

**This project does not work in the current state!**

bs.to regocnized automation since javascript property `navigator.webdriver` is set to `true`.
Overriding this property with javascript code (e.g. Object.defineProperty) does sort of work, but then one would have to solve an near infinite amount of CAPTCHAs.

There **is** a [possible fix](https://stackoverflow.com/questions/42169488/how-to-make-chromedriver-undetectable)
(version rollback to pre-Oct-2017, *very tedious*).

## Requirements

- python3.6 https://www.python.org/downloads/
- chromedriver https://chromedriver.chromium.org
- beautifulsoup4 `pip3.6 install beautifulsoup4`
- selenium `pip3.6 install selenium`
- requests `pip3.6 install requests`
- wget (only for downloading the videos)


## Getting started

1. Visit [bs.to](https://bs.to) and select your desired series (including season and language). Copy the URL in the top bar of your browser (Should be of this form: `http://bs.to/serie/<series>/<season>/<language>`, e.g. `https://bs.to/serie/Downton-Abbey/1/en`).
2. Run the program in the command-line: `python3.6 . [URL]`
3. Get video links from the output file(s)!


## Please note

- Currently only one host ([vivo.sx](https://vivo.sx)) is supported!

- Hosts like vivo **change** the video URLs frequently, so the links given only stay valid for a few hours.

- **Windows users**: Please user `Git Bash`/`PowerShell` instead of `cmd`!


## How it works

This tool uses selenium to parse and query html. It uses chromedriver to control a Chrome browser instance. This simulates a real user and browser. Conveniently this also allows **you** to solve the CAPTCHAs.


## Disclaimer

This tool does **not** store, stream or use copyrighted material - it only handles URLs.

Use of this tool is at each users own risk. Under no circumstances shall the developer(s) be liable for and indirect, incidental, consequential, special or exemplary damages arising out of the services this tool provides.
