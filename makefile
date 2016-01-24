# Beer Scraper 

lcbo:
	@echo "[`date +%H:%M:%S`] Running LCBO web crawler"
	@rm data/lcbo-data.json;
	@scrapy crawl lcbo-crawler -o data/lcbo-data.json -t json 2> logs/lcbo-`date +%y%m%d%H%M%S`.log
	@echo "[`date +%H:%M:%S`] Done"

all: lcbo

lint:
	@echo "[`date +%H:%M:%S`] Running Pylint"
	@pylint --rcfile=.pylintrc BeerScraper/** 1> logs/pylint-`date +%y%m%d%H%M%S`.log
	@echo "[`date +%H:%M:%S`] Done"
