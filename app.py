#%% imports
import requests
import pandas as pd
import json
from datetime import datetime, date

#%% Parametros 

# Suparametros
dia = 10
mes = 12
ano = 2020

date_start = f'{ano}-{mes}-{dia}'
date_end = ''
count = int(100)

url_path = f"https://old.west.albion-online-data.com/api/v2/stats/Gold?date={date_start}&end_date={date_end}&count={count}"

response = requests.get(url=url_path)
data = response.text

#%% Passando o json para um dataframe
df = pd.json_normalize(data, 'abc')

print(df)

# %%
data
# %%
