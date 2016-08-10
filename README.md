# WEG Crawler
Crawler to extract news from the [WEG](http://www.weg.net) site

## Installation

```sh
# Install pip
$ sudo apt-get install python-pip

# Install dependencies
$ pip install -r requirements.conf

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