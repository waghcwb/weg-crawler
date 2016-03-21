# WEB Crawler
> Crawler to extract notices from [WEG](http://www.weg.net) website

## Installation

Linux:

```sh
# Install pip
$ sudo apt-get install python-pip

# Install requests (use sudo if necessary)
$ pip install requests

# Install BeautifulSoup
$ pip install beautifulsoup4

# Make executables
$ sudo chmod +x scrapper.py images.py impex.py reset.sh
```

## Usage example
```sh
# Run the scrapper (will download all notices and content to 'dump.json')
$ ./scrapper.py

# Run the images downloader (will download all images based on the actual path to 'data/news/images')
$ ./images.py

# Run the .impex generator (will generate all impex files)
$ ./impex.py
```

## Meta

Wagner Souza - ([wagh.cwb@gmail.com](mailto:wagh.cwb@gmail.com))

[www.github.com/waghcwb/weg-crawler](https://github.com/waghcwb/weg-crawler)