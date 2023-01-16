# TutorCasesCrawler
## Introduction
There are 2 scrapers which each of them utilize different python tools. (Scrapy, Selenium)

Both extract lastest cases of private tutoring from 2 different websites. Scrapy extarct information by targeting HTML with XPath and CSS, or by sending request through API. Selenium extarct information by crawling through websites and find wanted information with XPath and CSS.

## Usage
Scrapy:
```
scrapy crawl tutor
```
Selenium:
```
python se.py
```

## Output format
A json file which has 7 fields per records. Result are encoded in etf-8 in order to display in Chinese.
```
{
  "source": "hktutor",
  "case_id": 1,
  "subject": "全科",
  "level": "中一",
  "price": "120",
  "venue": "灣仔",
  "remarks": null
}
```

## Status
Finished

## Future plan
* Add new features to Selenium scraper in order to scrape data on social media
