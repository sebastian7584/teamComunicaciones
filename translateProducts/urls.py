from django.urls import path
from .views import adminProductView, translateProductView

urlpatterns = [
    path('', adminProductView),
    path('admin', adminProductView),
    path('translate', translateProductView),
]
