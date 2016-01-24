# Beer Scraper 

# Linting

lcbo:
	scrapy crawl lcbo-crawler -o lcbo-data.json -t json 2> logs/lcbo-`date +%y%m%d%H%M%S`.log

all: lcbo

lint:
	pylint --rcfile=.pylintrc -f parseable BeerScraper/**
