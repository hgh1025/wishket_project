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
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

           
# class MyAPIView(APIView):
#     def get(self, response):
#         # GET 요청 처리 로직 구현
#         model= AWS_Usage.aws_usage(response)
#         serializer = AWSCostSerializer(model, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         # POST 요청 처리 로직 구현
#         monthly_data = AWS_Bill.aws_bill(monthly_data)
#         serializer = AWSCostSerializer(monthly_data, many=True)  
#         return Response(serializer.data)

#사용 내역 조회 API 명세 
class AWS_Usage(APIView):
    def get_filtered_data(year, month):
        # 데이터 압축 파일 URL
        url = "http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip"
        response = requests.get(url)
        
        # 압축 파일을 엽니다.
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            # 압축을 푼 후 csv 파일을 읽습니다.
            with zip_ref.open('coding_test_1.csv','r') as csv_file:
                df = pd.read_csv(io.TextIOWrapper(csv_file, encoding='utf-8'))
    
        # year와 month로 필터링합니다.
        mask = (df['TimeInterval'].str[:7] == f'{year}-{month}')
        filtered_df = df.loc[mask]
        print(mask)
        # 필터링된 결과를 csv 파일로 저장합니다.
        filtered_df.to_csv('usage.csv', index=False, encoding='utf-8-sig')
    
        # csv 파일의 내용을 반환합니다.
        with open('usage.csv', 'r', encoding='utf-8-sig') as f:
            return f.read()
    #get_filtered_data(2022,11)  -> 해당조건에 맞는 csv파일 출력 확인 .!
    
    #예외처리 로직
    @api_view(['GET'])
    def aws_usage(request):
        
        year = request.GET.get('year')
        month = request.GET.get('month')
            
        # c.예외 처리 (2) -> year와 month 파라미터가 없는 경우 에러 메시지를 반환
        if not year or not month:
            return HttpResponse('year 또는 month가 입력되지 않았습니다.', status=400)
        
        # c.예외 처리 (1) -> 데이터 url이 없는 경우 에러 메세지를 반환 
        try:
            result = AWS_Usage.get_filtered_data(year, month)
        except urllib.error.HTTPError:
            return HttpResponse('데이터 URL에 파일이 없습니다.', status=404)
        except zipfile.BadZipFile:
            return HttpResponse('데이터 URL의 압축 파일이 올바르지 않습니다.', status=500)
        
        # c.예외 처리 (3) -> 다운로드한 파일이 10MB를 넘는 경우 에러 메시지를 반환
        if len(result.encode('utf-8')) > 10 * 1024 * 1024:
            return HttpResponse("file size exceeds the limit of 10MB", status=400)
         
         # csv 파일을 반환합니다.    
        response = HttpResponse(result, content_type='text/csv')
        
        #csv로 저장된 filename 지정
        response['Content-Disposition'] = f'attachment; filename=usage.csv'
        return Response(response, status=200)   
        
        #직렬화로 인해 orderedDict로 변환
        # serializer = AWSCostSerializer(result, many=True)
        # #JSON파일로 변환하여 get으로 데이터를 보여준다.
        # content = JSONRenderer().render(serializer.data)
        # return JsonResponse(content, status=200)

        
#사용 요금 조회 API  명세 
class AWS_Bill(APIView):
    def get_filtered_data(id, year, month):
        # 데이터 압축 파일 URL
        url = "http://dtgqz5l2d6wuw.cloudfront.net/coding_test_2.zip"
        response = requests.get(url)
        
        # # 압축 파일을 저장할 경로
        # zip_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.zip')
        # # 압축 파일을 다운로드합니다.
        # urllib.request.urlretrieve(url, zip_file_path)

        # 압축 파일을 엽니다.
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            # 압축을 푼 후 csv 파일을 읽습니다.
            with zip_ref.open('coding_test_2.csv','r') as csv_file:
                df = pd.read_csv(io.TextIOWrapper(csv_file, encoding='utf-8'))

        # id, year, month로 필터링합니다.
        mask = (df['userId'] == id) & (df['TimeInterval'].str[:4] == year)
        if month:
            mask &= (df['TimeInterval'].str[5:7] == month)
        filtered_df = df.loc[mask]

        return filtered_df

    @api_view(['POST'])
    def aws_bill(request):
        id = request.POST.get('id')
        year = request.POST.get('year')
        month = request.POST.get('month')

        if not id or not year:
            return HttpResponse('id 또는 year가 입력되지 않았습니다.', status=400)

        try:
            filtered_df = AWS_Bill.get_filtered_data(id, year, month)
        except urllib.error.HTTPError:
            return HttpResponse('데이터 URL에 파일이 없습니다.', status=404)
        except zipfile.BadZipFile:
            return HttpResponse('데이터 URL의 압축 파일이 올바르지 않습니다.', status=500)

        # 각 월별로 분리합니다.
        monthly_data = {}
        for i in range(1, 13):
            month_str = f'{i:02}'
            monthly_filtered_df = filtered_df[filtered_df['TimeInterval'].str[5:7] == month_str] 
            if len(monthly_filtered_df) == 0:
                continue

            # 환율, 요금, 원화 요금을 계산합니다.
            exchange_rate = round(monthly_filtered_df['exchangeRate'].mean(), 8) #월별 환율(exchange_rate): 조건 내 모든 행의 exchangeRate 평균
            cost = monthly_filtered_df['cost'].sum() # 요금(cost): 조건 내 모든 행의 cost 합계
            cost_krw = int(round((monthly_filtered_df['exchangeRate'] * monthly_filtered_df['cost']).sum(), 2))#한화 요금(cost_krw): 조건 내 각 행의 exchangeRate * cost 값에 대한 모든 행의 합계
            
            #JSON 형태로 만들어 놓음.
            monthly_data[month_str] = {
                'exchange_rate': exchange_rate,
                'cost': cost,
                'cost_krw': cost_krw
            }

      
        #JSON형태를 OrderedDict 형태로 변환
        stream = io.BytesIO(monthly_data)
        data = JSONParser().parse(stream)
        
        #  OrderedDict 형태로 db에 저장.
        serializer = AWSCostSerializer(data, data = request.data)
        #유효성 검사
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
        



