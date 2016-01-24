# Beer Scraper 


lcbo:
	@if [ ! -d logs ]; then \
		mkdir logs; \
	fi
	@rm -f data/lcbo-data.json;
	@echo "[`date +%H:%M:%S`] Running LCBO web crawler"

	@scrapy crawl lcbo-crawler -o data/lcbo-data.json -t json 2> logs/lcbo-`date +%y%m%d%H%M%S`.log
	@echo "[`date +%H:%M:%S`] Done"

saq:
	@if [ ! -d logs ]; then \
		mkdir logs; \
	fi
	@rm -f data/saq-data.json;
	@echo "[`date +%H:%M:%S`] Running LCBO web crawler"

	@scrapy crawl saq-crawler -o data/saq-data.json -t json 2> logs/saq-`date +%y%m%d%H%M%S`.log
	@echo "[`date +%H:%M:%S`] Done"

all: lcbo saq

lint:
	@echo "[`date +%H:%M:%S`] Running Pylint"
	@pylint --rcfile=.pylintrc BeerScraper/** 1> logs/pylint-`date +%y%m%d%H%M%S`.log
	@echo "[`date +%H:%M:%S`] Done"
