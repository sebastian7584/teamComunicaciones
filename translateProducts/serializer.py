from rest_framework import serializers
from .models import TranslateProduct

class TranslateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslateProduct
        fields = '__all__'
    