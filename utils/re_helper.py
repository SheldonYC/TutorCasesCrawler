import re

# Extract only number inside given string
def FilterInt(string):
  return int(re.findall(r"\d+", string)[0])