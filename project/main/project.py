from django.shortcuts import render , redirect
from django.http import HttpResponse, HttpResponseBadRequest
import csv
import requests
import io
import zipfile
import os
import pandas as pd

url = 'http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip'
response = requests.get(url)
file = io.BytesIO(response.content)
df_result = pd.read_csv(file, 'utf-8')
# with io.BytesIO(response.content) as f:
#         with zipfile.ZipFile(f) as zip_file:
#             with zip_file.open('coding_test_1.csv') as csv_file:
#                 data = list(csv.DictReader(io.TextIOWrapper(csv_file, 'utf-8')))
#                 df_result = pd.read_csv(data)
#                 writer = csv.DictWriter(response, fieldnames=data[0].keys())
#                 writer.writeheader()
#                 writer.writerows(df_result)
                
#                 return response
                
# print(file.status_code)
# print(file.content)
# print(type(file.content))
print(df_result)