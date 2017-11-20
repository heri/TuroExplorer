# TuroExplorer

Like many other modern sites, Turo and AirBnb use heavily javascript. Simple scraping returns blank results. dryscrape use a headless browser to render javascript before we get the html

On Mac, webkit-server requires `qt<=5.5` since qt 5.6 removes the WebKit module
* `brew install qt@5.5`
* `easy_install pip`
* `pip install dryscrape`

Ubuntu
* `apt-get install qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb`

TODOS

* bug : gets node instead of text content
* save to postgres
* multiple geographical regions