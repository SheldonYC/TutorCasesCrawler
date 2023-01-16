import json

def GetURL(driver, url):
  try:
    driver.get(url)
  except Exception as e:
    print(e)

def WriteToJSON(name, data):
  records = json.dumps(data, ensure_ascii=False, indent = 2)
  tutor_records = open(name, "w", encoding="utf8")
  tutor_records.write(records)
  tutor_records.close()