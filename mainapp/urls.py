from django.urls import path
from . import views  # Це дозволить файлу "бачити" твій views.py

urlpatterns = [
    path('', views.home, name='home'),
    path('other/', views.other_page, name='other'),
]