import scrapy
import urllib
import json

# import item instance from parent dir
from ..items import TutorscraperItem

# This spider will
# 1) Crawl to tutor case website
# 2) Fetch, preprocess and store data in JSON
# 3) decode unicode and store as English
class TutorCase(scrapy.Spider):
  name = "tutor"
  case_id = 1

  def start_requests(self):
    urls = ["https://www.hktutor.hk/", "https://www.hkta.edu.hk/jobcase"]
    # Go to all wanted stock page and scrape
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    # parse for hktutor, with css
    if "hktutor" in response.url:
      items = TutorscraperItem()
      for table in response.css('table.center.no_padding.main_table'):
        items["source"] = "hktutor"
        items["case_id"] = self.case_id
        items["subject"] = table.css('tr[style="font-size:14px"] td[style="padding:0px 0px 0px 20px;"]::text').get()
        items["level"] = table.css('tr[style="font-size:14px"] td[colspan="2"]::text').get()[:2]
        items["price"] = table.css('tr[style="font-size:14px"] td[style="padding:0px 0px 0px 20px;"] span::text').get().replace('$','')
        items["venue"] = table.css('tr[style="font-size:16px;font-weight:"] td[width="116"]::text').get() + " " + table.css('tr[style="font-size:16px;font-weight:"] td[width="192"]::text').get().replace('\n','')
        items["remarks"] = table.css('tr[style="font-size:14px"] td[colspan="4"]::text').get()
        self.case_id = self.case_id + 1
        yield items
      
      # go next page
      next_page = response.xpath('/html/body/div[2]/div[2]/div[1]/table/tr/td[7]/a/@href').extract()[0]
      next_page = urllib.parse.urljoin(response.url, next_page)
      # check if it is not last page
      if next_page != response.url:
        yield response.follow(url=next_page, callback=self.parse)

    # Parser for hkta, with API hijack
    elif "hkta" in response.url:
      # filtered math/phy/chem/m2, in TKO
      api = 'https://www.hkta.edu.hk/api/es/job/search?pageNum=1&areaId=10618&areaTexts=%E5%B0%87%E8%BB%8D%E6%BE%B3&subject=tutor_remediation_math,tutor_remediation_math_m2,tutor_remediation_physical,tutor_remediation_chemistry&subjectLabels=%E6%95%B8%E5%AD%B8,%E6%95%B8%E5%AD%B8%EF%BC%88M2%EF%BC%89,%E7%89%A9%E7%90%86,%E5%8C%96%E5%AD%B8&pageSize=20&lang=zh_TW'
      yield scrapy.http.JsonRequest(url=api, callback=self.parse_api)

  def parse_api(self, response):
    items = TutorscraperItem()
    data = json.loads(response.body)
    if "hkta" in response.url:
      for record in data["data"]["list"]:
        items["source"] = "hkta"
        items["case_id"] = record["jobNo"]
        items["subject"] = record["subjectName"]
        items["level"] = record["studentTutorialSubject"]
        items["price"] = record["studentCharge"]
        items["venue"] = record["address1"]
        items["remarks"] = record["remarks"]
        yield items
