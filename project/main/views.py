from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view #함수형 뷰 형태로 작성하려면 api_view 
from rest_framework.views import APIView #클래스형 뷰로 바꾸면 APIView(매서드를 조건문 대신 함수로 정의)
from rest_framework.response import Response
from .models import AWSCost
from .serializers import AWSCostSerializer
from rest_framework import status
import pandas as pd
import requests
import csv
import io
import zipfile
import math
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import urllib.request
import os
import json

# def viewJson(request):
#     return JsonResponse("rest api and point", safe= False)

# @api_view(['GET']) 
# def index(request):
       
   
    
#     api_urls= {
#        'List' : '/list/' ,
#        'Detail' : '/detail',
#        }
       
#     urls= {
#        'index' : '/' ,
#        'app' : '/app',
#        }   
#     context = dict()
#     context['api_urls'] =api_urls
#     context['urls'] =urls
#     return Response(context)
    
# @api_view(['GET']) 

# def aws_usage(request):
#     # 요청에서 year와 month 파라미터를 가져옴
    
#     year = request.GET.get('year') #<--- 둘 중 무엇이 맞는지 확인 필요
#     month = request.GET.get('month')
#     # year = int(AWSCost.objects.filter(start_time__year=year)) #<--- 둘 중 무엇이 맞는지 확인 필요
#     # month = int(AWSCost.objects.filter(start_time__month=month))
    
#     # AWS 데이터 조회 API URL
#     url = 'http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip'
#     # req_parameter = {'year':'YYYY', 'month':'MM'}
#     # response = requests.get(url, params = req_parameter)
#     response = requests.get(url)
    

    
#     # b.API 로직 /파일 해제 및 필터링
#     try:
#         with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
#             # 압축 파일 내의 csv 파일 이름 'coding_test_1.csv'
            
#             # csv 파일 열기
#             with zip_file.open('coding_test_1.csv', 'r') as csv_file:
#                 # # csv 파일 읽기
#                 df = pd.read_csv(io.TextIOWrapper(csv_file, encoding='utf-8')) # 필터링을 위해 df로 변환 및 한글 출력
        
#     #     #필터링 된 year, month list 만들기
#                 filtered_year= []        
#                 filtered_month= []       
#                 for i in range(len(df['TimeInterval'])): # len(df['TimeInterval'] - >8818
#                     #time_interval_start == '2022-11-01T00:00:00Z'
#                     time_interval_start = df['TimeInterval'].str.split('/')[i][0] # 해당 값이 파라미터의 year, month 값이 일치
#                     #row_year ==2022 , row_month == 11
#                     row_year, row_month, _ = time_interval_start.split('-')
#                     row_year=int(row_year) # 정수로 변경, row_year ==2022
#                     row_month=int(row_month) # 정수로 변경, row_month == 11
            
#                     filtered_year= []        
#                     filtered_month= []
#                     filtered_year.append(row_year)
#                     filtered_month.append(row_month)
#                     df['year'] = filtered_year
#                     df['month'] = filtered_month
#                     #!! 추가 - > 필터링된 결과 값을 csv 파일로 반환합니다. 
#                 #     csv_reader= df.to_csv('coding_test_1.csv', sep=" ", encoding = "cp949")
#                 # # 파일 이름 설정 ContentType: text/csv, Filename: usage.csv
#                 #     response = HttpResponse(content_type='text/csv')
#                 #     response['Content-Disposition'] = f'attachment; filename="usage.csv"'
#                 #     writer = csv.DictWriter(response, fieldnames=csv_reader.fieldnames)
#                 #     writer.writeheader()
#                 #     writer.writerows(filtered_year,filtered_month)
#                     context = dict()
#                     return Response(df)
#     except:
#         pass
                
#                 # # c.예외 처리 /파일 다운로드
#                 # try:
#                 #     response = requests.get(url) # 필터링된 df를 가져옴
                    
#                 # # c.예외 처리 (1) -> 데이터 url이 없는 경우 에러 메세지를 반환  
#                 #     if response.status_code == 404:
#                 #         return HttpResponse("file not found", status=404)
                    
#                 #     # c.예외 처리 (2) -> year와 month 파라미터가 없는 경우 에러 메시지를 반환
#                 #     if year != start_time.year or month != start_time.month:
#                 #         return HttpResponse("year and month parameters are required", status=400)
                     
#                 #     # c.예외 처리 (3) -> 다운로드한 파일이 10MB를 넘는 경우 에러 메시지를 반환
#                 #     content_length = response.headers.get('Content-Length')
#                 #     if content_length and int(content_length) > 10 * 1024 * 1024:
#                 #         return HttpResponse("file size exceeds the limit of 10MB", status=400)
                
#                 # # + c.예외 처리 (4) -> 그 외에 알 수 없는 에러인 경우
#                 # except response.status_code != 200:
#                 #     return HttpResponse("file not found", status=404)
 
# #사용 내역 조회 API
#     # def filter_date(filtered_year, filtered_month):
       
        
#     #     #data 열기
#     #     data_url = 'http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip'
#     #     response = requests.get(data_url)
        
#     #     with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file: #압축해제
#     #         with zip_file.open('coding_test_1.csv','r') as csv_file: # 읽기 모드로 open
#     #             df = pd.read_csv(io.TextIOWrapper(csv_file, encoding='utf-8')) # 필터링을 위해 df로 변환 및 한글 출력
        
#     #     #필터링 된 year, month list 만들기
#     #     filtered_year= []        
#     #     filtered_month= []       
#     #     for i in range(len(df['TimeInterval'])): # len(df['TimeInterval'] - >8818
#     #         #time_interval_start == '2022-11-01T00:00:00Z'
#     #         time_interval_start = df['TimeInterval'].str.split('/')[i][0] # 해당 값이 파라미터의 year, month 값이 일치
#     #         #row_year ==2022 , row_month == 11
#     #         row_year, row_month, _ = time_interval_start.split('-')
#     #         row_year=int(row_year) # 정수로 변경, row_year ==2022
#     #         row_month=int(row_month) # 정수로 변경, row_month == 11
    
#     #         filtered_year= []        
#     #         filtered_month= []
#     #         filtered_year.append(row_year)
#     #         filtered_month.append(row_month)
#     #         df['year'] = filtered_year
#     #         df['month'] = filtered_month
#     #         #!! 추가 - > 필터링된 결과 값을 csv 파일로 반환합니다. 
#     #         df.to_csv('coding_test_2.csv', sep=" ", encoding = "cp949")
    
# # def filter_user(request, userId):
# #     id = request.GET.get('userId')
# #     if userId == id:
# #         pass 

# # def aws_usage(request):
# #     year = request.GET.get('year')
# #     month = request.GET.get('month')
# #     if not year or not month:
# #         return HttpResponseBadRequest('year and month parameters are required.')
    
# #     url = 'http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip'
# #     response = requests.get(url, stream=True)
    
# #     if not response.ok:
# #         return HttpResponseBadRequest('Failed to download data from the server.')
    
# #     content_length = response.headers.get('Content-Length')
# #     if content_length and int(content_length) > 10*1024*1024:
# #         return HttpResponseBadRequest('The size of the compressed file exceeds 10MB.')
    
# #     with io.BytesIO(response.content) as f:
# #         with zipfile.ZipFile(f) as zip_file:
# #             with zip_file.open('coding_test_1.csv') as csv_file:
# #                 data = list(csv.DictReader(io.TextIOWrapper(csv_file, 'utf-8')))
# #                 filtered_data = filter_date(year, month, data)
# #                 if not filtered_data:
# #                     return HttpResponseBadRequest(f'No data for {year}-{month}.')
# #                 response = HttpResponse(content_type='text/csv')
# #                 response['Content-Disposition'] = f'attachment; filename=usage.csv'
# #                 writer = csv.DictWriter(response, fieldnames=data[0].keys())
# #                 writer.writeheader()
# #                 writer.writerows(filtered_data)
# #                 return response
    
# # import requests
# # import zipfile
# # import csv
# # from django.http import HttpResponse
# # from django.views.decorators.http import require_http_methods


# # #사용 요금 조회 API 명세
# # @require_http_methods(["GET"])
# # def aws_usage(request):
# #     # Check if year and month parameters are provided
# #     year = request.GET.get('year')
# #     month = request.GET.get('month')
# #     if not year or not month:
# #         return HttpResponse('Year and month parameters are required.', status=400)

# #     # Download and extract data file
# #     data_url = 'http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip'
# #     req_parameter = {'year':'YYYY', 'month':'MM'}
# #     response = requests.get(data_url, params = req_parameter)
# #     if response.status_code != 200:
# #         return HttpResponse('Failed to download data file.', status=500)
# #     if int(response.headers['Content-Length']) > 10 * 1024 * 1024:
# #         return HttpResponse('Data file is too large.', status=500)
# #     with zipfile.ZipFile(io.BytesIO(response.content)) as z:
# #         with z.open('coding_test_1.csv') as f:
# #             reader = csv.reader(io.TextIOWrapper(f, encoding='utf-8'))
# #             rows = list(reader)
# #             # Filter rows by year and month
# #             filtered_rows = [row for row in rows if row[0].startswith(f'{year}-{month}')]
# #             if not filtered_rows:
# #                 return HttpResponse('No data found for the specified year and month.', status=404)
# #             # Build response CSV file
# #             response = HttpResponse(content_type='text/csv')
# #             response['Content-Disposition'] = f'attachment; filename="usage.csv"'
# #             writer = csv.writer(response)
# #             writer.writerows(rows)
# #             return response
            
# # #제공된 데이터 압축 파일 내 데이터를 아래 조건으로 필터링 합니다.
# # #TimeInterval(데이터 형식: 시작시간/종료시간)의 시작 시간 내 연도와 form-data의 year 값이 일치
# # # def filter_data1(year, month, data):
    
# # #userId값이 form-data의 id와 값이 일치
# # #(optional) TimeInterval(데이터 형식: 시작시간/종료시간)의 시작 시간 내 월과 form-data의 month 값이 일치

# # import pandas as pd

# # data_url = 'http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip'
# # response = requests.get(data_url)

# # with zipfile.ZipFile(io.BytesIO(response.content)) as z:
# #     with z.open('coding_test_1.csv') as f:
# #         df = pd.read_csv(io.TextIOWrapper(f, encoding='utf-8'))

# # print(df['TimeInterval'])

#      # @api_view(['GET']) 
#     # def aws_usage(request):
#     #     # 요청에서 year와 month 파라미터를 가져옴
        
#     #     year = int(request.GET.get('year')) #<--- 둘 중 무엇이 맞는지 확인 필요
#     #     month = int(request.GET.get('month'))
#     #     # year = int(AWSCost.objects.filter(start_time__year=year)) #<--- 둘 중 무엇이 맞는지 확인 필요
#     #     # month = int(AWSCost.objects.filter(start_time__month=month))
        
#     #     # AWS 데이터 조회 API URL
#     #     url = 'http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip'
#     #     req_parameter = {'year':'YYYY', 'month':'MM'}
#     #     response = requests.get(url, params = req_parameter)
        
        
    
        
#     #     # b.API 로직 /파일 해제 및 필터링
#     #     try:
#     #         with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
#     #             # 압축 파일 내의 csv 파일 이름 'coding_test_1.csv'
                
#     #             # csv 파일 열기
#     #             with zip_file.open('coding_test_1.csv', 'r') as csv_file:
#     #                 # # csv 파일 읽기
#     #                 csv_reader = csv.reader(io.TextIOWrapper(csv_file, encoding='utf-8'))
                 
#     #                 #필터링 된 year, month list 만들기
#     #                 filtered_rows= []        
                           
#     #                 for row in csv_reader:
#     #                     start_time = datetime.strptime(row['TimeInterval'].split('/')[0], '%Y-%m-%d %H:%M:%S')
#     #                     if start_time.year == year and start_time.month == month:
#     #                         filtered_rows.append(row)
            
#     #                 context = dict()   
#     #                 context['filtered_year'] = filtered_rows[0:4]
#     #                 context['filtered_month'] = filtered_rows[5:7]
#     #                 # 파일 이름 설정 ContentType: text/csv, Filename: usage.csv
#     #                 response = HttpResponse(content_type='text/csv')
#     #                 response['Content-Disposition'] = f'attachment; filename="usage.csv"'
#     #                 writer = csv.DictWriter(response, fieldnames=csv_reader.fieldnames)
#     #                 writer.writeheader()
#     #                 writer.writerows(filtered_rows)
#     #                 # return response
    
                    
#     #                 # c.예외 처리 /파일 다운로드
#     #                 try:
#     #                     response = requests.get(url, params = req_parameter) # 필터링된 df를 가져옴
                        
#     #                 # c.예외 처리 (1) -> 데이터 url이 없는 경우 에러 메세지를 반환  
#     #                     if response.status_code == 404:
#     #                         return HttpResponse("file not found", status=404)
                        
#     #                     # c.예외 처리 (2) -> year와 month 파라미터가 없는 경우 에러 메시지를 반환
#     #                     if year != start_time.year or month != start_time.month:
#     #                         return HttpResponse("year and month parameters are required", status=400)
                         
#     #                     # c.예외 처리 (3) -> 다운로드한 파일이 10MB를 넘는 경우 에러 메시지를 반환
#     #                     content_length = response.headers.get('Content-Length')
#     #                     if content_length and int(content_length) > 10 * 1024 * 1024:
#     #                         return HttpResponse("file size exceeds the limit of 10MB", status=400)
                    
#     #                 # + c.예외 처리 (4) -> 그 외에 알 수 없는 에러인 경우
#     #                 except response.status_code != 200:
#     #                     return HttpResponse("file not found", status=404)
#     #     except:
#     #         pass
#     #     return Response(context)





# class AWS_Bill(APIView):

#     # def get(self,request, user_id): #정보
#     #     model = AWSCost.objects.get(user_id = user_id)
#     #     serializer = AWSCostSerializer(model)
#     #     return Response(serializer.data)
        
#     # def put(self, request, user_id): #수정
#     #     model = AWSCost.objects.get(user_id = user_id)
        
#     #     serializer = AWSCostSerializer(model, data = request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status = status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
#     # def delete(self,request, user_id): #삭제
#     #     model = AWSCost.objects.get(user_id = user_id)
#     #     model.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)
        
#     # def post(self, request): #추가
    
#     #     serializer = AWSCostSerializer(data = request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status = status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
#     def filter_date(filtered_year, filtered_month,exchange_rate,cost,cost_krw_list):
#        #필터링 된 year, month list 만들기
#         filtered_year= []        
#         filtered_month= []
       
#        #data 열기
#         data_url = 'http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip'
#         response = requests.get(data_url)
       
#         with zipfile.ZipFile(io.BytesIO(response.content)) as z:
#             with z.open('coding_test_1.csv') as f:
#                 df = pd.read_csv(io.TextIOWrapper(f, encoding='utf-8'))
#         for i in range(len(df['TimeInterval'])): # len(df['TimeInterval'] - >8818
#            #time_interval_start == '2022-11-01T00:00:00Z'
#             time_interval_start = df['TimeInterval'].str.split('/')[i][0] # 해당 값이 파라미터의 year, month 값이 일치
#            #row_year ==2022 , row_month == 11
#             row_year, row_month, _ = time_interval_start.split('-')
#             row_year=int(row_year) # 정수로 변경, row_year ==2022
#             row_month=int(row_month) # 정수로 변경, row_month == 11

#             filtered_year= []        
#             filtered_month= []
#             filtered_year.append(row_year)
#             filtered_month.append(row_month)
#             print(filtered_year)
           
#          #환율에 대한 필터링 필요.  
            
#             #  1. 월별 환율(exchange_rate) - > list로 변환 필요 - >월별 그룹핑 필요
#             exchange_rate = df['exchangeRate'].mean(axis=0)
#             exchange_rate
#             # 2. 요금(cost): 조건 내 모든 행의 cost 합계  - > list로 변환 필요 - >월별 그룹핑 필요
#             cost = df['Cost'].sum()
#             cost
#             # 3. 한화 요금(cost_krw): 조건 내 각 행의 exchangeRate * cost 값에 대한 모든 행의 합계
#             df_cost_krw = df['exchangeRate'] * df['Cost'].sum()
#             n= list(df_cost_krw)

#             cost_krw_list = []
#             for i in range(len(n)):
#                 cost_krw = np.floor(n[i]*100) / 100 #소수점 2의 자리에서 버림을 수행합니다.
#                 cost_krw_list.append(cost_krw)
        
#         @api_view(['GET'])   
#         def aws_bill(request, year, month, id):
#             id = request.GET.get('id')
#             year = request.GET.get('year')
#             month = request.GET.get('month')
#             # id = int(AWSCost.objects.filter(user_id=id))
#             # year = int(AWSCost.objects.filter(start_time__year=year))
#             # month = int(AWSCost.objects.filter(start_time__month=month))
#             url = 'http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip'
#             # form_data = ??
            
#             #예외처리
#             try:
#                 response = requests.get(url)
#              # c.예외 처리 (4) -> 데이터 URL의 파일에 환율 정보가 없는 경우  
#                 if not data['exchange_rate']:
#                     return HttpResponse("There is no exchange rate information in the data file at the data URL.")
                    
#             # c.예외 처리 (4) -> 그 외에 알 수 없는 에러인 경우
#             except response.status_code != 200:
#                 return HttpResponse("file not found", status=404) 
            
            
            
#             # b.API 로직 /파일 해제 및 필터링 
#             try:
#                 with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
#                     # 압축 파일 내의 csv 파일 이름 'coding_test_1.csv'
                    
#                     # csv 파일 열기
#                     with zip_file.open('coding_test_1.csv', 'r') as csv_file:
#                         # # csv 파일 읽기
#                         csv_reader = csv.reader(io.TextIOWrapper(csv_file, encoding='utf-8'))
                      
#                         data = list(csv.DictReader(io.TextIOWrapper(csv_reader, 'utf-8')))
                        
            
#             except response.status_code != 200:
#                 return HttpResponse("file not found", status=404) 
#             # 필수 입력값이 누락되었는지 확인
        
#             if not id or not year:
#                 return Response({'error': 'id and year are required fields'})
        
#             # 데이터 필터링
          
#             if month:
#                 aws_costs = aws_costs.filter(start_time__month=month)
        
#             # 데이터가 없을 경우 예외 처리
#             if not aws_costs:
#                 return Response({'error': 'No data found for the given input'})
        
#             # 월별 데이터 계산
#             data = {}
#             for aws_cost in aws_costs:
#                 month = aws_cost.start_time.strftime('%m')
#                 if month not in data:
#                     data[month] = {
#                         'exchange_rate': aws_cost.exchange
#                     }
                    
                
#             #json 파일로 변환하기
#             serializer = AWSCostSerializer(data, many=True)
#             return Response(serializer.data)
