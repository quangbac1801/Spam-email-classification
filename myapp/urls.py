from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_spam, name='home'),  # Trang mặc định của ứng dụng
]
