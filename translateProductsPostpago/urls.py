from django.urls import path
from .views import adminProductPostpagoView, translateProductPostpagoView

urlpatterns = [
    path('admin', adminProductPostpagoView),
    path('translate', translateProductPostpagoView),
    
]
