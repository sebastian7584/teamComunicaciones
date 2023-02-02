from rest_framework import serializers
from .models import TranslateProductPostpago

class TranslateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslateProductPostpago
        fields = '__all__'
    