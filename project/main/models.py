from django.db import models
from .models import*
# Create your models here.


class AWSCost(models.Model):
    user_id = models.CharField(max_length=12)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    usage_type = models.CharField(max_length=255)
    usage_quantity = models.IntegerField()
    cost = models.IntegerField()
    currency_code = models.CharField(max_length=3)
    exchange_rate = models.IntegerField()