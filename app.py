# imports
import requests

# Parametros 
date_start = ''
date_end = ''
count = ''

url_path = "https://old.west.albion-online-data.com/api/v2/stats/Gold?date=2025-10-22&end_date=2026-01-22&count=1"


r = requests.get(url=url_path)
print(r.text)
