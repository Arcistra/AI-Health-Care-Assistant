from django.urls import path
from HealthCareapp import views

urlpatterns = [
    path('', views.admin_page, name='admin_page'),
]