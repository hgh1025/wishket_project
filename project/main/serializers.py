from rest_framework import serializers
from .models import AWSCost


class AWSCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AWSCost
        fields = '__all__'
        
serializer = AWSCostSerializer(AWSCost)




class AWSCostSerializer(serializers.Serializer):
    #필드 = serializers.필드타입
    user_id = serializers.CharField(max_length=12)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    usage_type = serializers.CharField(max_length=255)
    usage_quantity = serializers.FloatField()
    cost = serializers.FloatField()
    currency_code = serializers.CharField(max_length=3)
    exchange_rate = serializers.FloatField()
    def create(self, validated_data):
        return AWSCost.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        # instance.필드 = validated_data.get("필드", instance.필드)
        instance.user_id = validated_data.get("user_id", instance.user_id)
        instance.start_time = validated_data.get("start_time", instance.start_time)
        instance.end_time = validated_data.get("end_time", instance.end_time)
        instance.usage_type = validated_data.get("usage_type", instance.usage_type)
        instance.usage_quantity = validated_data.get("usage_quantity", instance.usage_quantity)
        instance.cost = validated_data.get("cost", instance.cost)
        instance.currency_code = validated_data.get("currency_code", instance.currency_code)
        instance.exchange_rate = validated_data.get("exchange_rate", instance.exchange_rate)
        instance.save()
        return instance

