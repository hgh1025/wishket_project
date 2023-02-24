from django.urls import path
from . import views, api

urlpatterns = [
    path('', views.index, name= 'index'),
   path('viewJson', views.viewJson, name= 'viewJson'),
    path('aws_usage', views.aws_usage, name= 'aws_usage'),
]