from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import GetURL, FilterInt, WriteToJSON

# This spider will:
# 1) go to tutorok and scrape all pages by clicking next page button
# 2) go to tutorcircle and scrape all pages with filter on
# 3) export data in json in utf-8 for later merging

# setting of driver (Chrome, no image, default wait time = 10s)
options = webdriver.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

hasNextPage_tutorok = True
hasNextPage_tutorcircle = True
total_cases = 0
data = []

def FetchTutorok(remaining_cases):
  # a page has maximum of 15 items
  remaining_cases = min(remaining_cases, 15)
  # fetch data request
  content_table = driver.find_elements(By.XPATH,'/html/body/div/div[3]/div[2]/div/div[3]/table/tbody/tr')[1:]
  # parsing data into dict
  for row in content_table:
    items = row.text.split(" ")
    item = {}
    item["source"] = "tutorok"
    item["case_id"] = items[0]
    item["subject"] = items[3]
    item["price"] = items[5]
    item["level"] = items[2]
    item["venue"] = items[1]
    item["remarks"] = items[8]
    data.append(item)

def FetchTutorcircle():
  content_table = driver.find_elements(By.XPATH,'//*[@id="accordion5"]/div/div[contains(@id, "collapse")]')
  for row in content_table:
    item = {}
    item["source"] = "tutorcircle"
    item["case_id"] = row.get_attribute("data-caseid")
    item["subject"] = row.get_attribute("data-subject")
    item["price"] = row.get_attribute("data-complete-fee")
    item["level"] = row.get_attribute("data-year")
    item["venue"] = row.get_attribute("data-locationdistricts")
    item["remarks"] = row.get_attribute("data-caselocationtype")
    data.append(item)
  return

def filter_subject():
  # wait for content to load
  old_content = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="0"]')))
  # open filter menu
  filter_btn = wait.until(EC.element_to_be_clickable((By.ID, 'tut_subject')))
  filter_btn.click()
  math_filter = wait.until(EC.element_to_be_clickable((By.ID, 'radio_tutor_core_2')))
  math_filter.click()
  # open elective menu
  elective_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headingSix"]/h4/a')))
  elective_btn.click()
  # filter for maths, M2, physics, chemistry
  physics_filter = wait.until(EC.element_to_be_clickable((By.ID, 'radio_tutor_sci_0')))
  physics_filter.click()
  chemistry_filter = wait.until(EC.element_to_be_clickable((By.ID, 'radio_tutor_sci_1')))
  chemistry_filter.click()
  m2_filter = wait.until(EC.element_to_be_clickable((By.ID, 'radio_tutor_sci_4')))
  m2_filter.click()
  # confirm changes
  confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Modal_Tut_Subject"]/div/div/div[3]/div/button[2]')))
  confirm_btn.click()
  # wait for the filter to apply
  wait.until(EC.staleness_of(old_content))

# scraping tutorok
GetURL(driver, "https://www.tutorok.com/")
total_cases = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div/div[2]/span[2]").text
total_cases = FilterInt(total_cases)
while hasNextPage_tutorok:
  FetchTutorok(total_cases)
  total_cases = total_cases - 15
  # go to next page if exist
  next_page_btn = driver.find_element(By.ID, "a_next")
  if next_page_btn.is_displayed():
    next_page_btn.click()
  else:
    hasNextPage_tutorok = False
# print("Finished scraping tutorok")

# scraping tutorcircle
GetURL(driver, "https://www.tutorcircle.hk/case-list.php")
filter_subject()
while hasNextPage_tutorcircle:
  FetchTutorcircle()
  hasNextPage_tutorcircle = False
  next_page_btn = driver.find_element(By.XPATH, '//*[@id="pagination"]/div/div/ul/li[last()]')
  if "disabled" in next_page_btn.get_attribute("class"):
    hasNext_tutorcircle = False
  else:
    old_content = driver.find_element(By.XPATH, '//*[@id="0"]')
    next_page_btn.click()
    wait.until(EC.staleness_of(old_content))

driver.quit()
WriteToJSON("tutor.json", data)