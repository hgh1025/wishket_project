from django.contrib import admin
from django.urls import path, include
from main.api import AWS_Bill , AWS_Usage



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('aws/usage/', AWS_Usage.as_view(), name='aws-usage'),
    path('aws/bill/', AWS_Bill.as_view(), name='aws-bill'),
    # path('aws/bill/<int:user_id>', AWS_Bill.as_view(), name='aws-bill'),
    path('',include('main.urls')),
    
]
