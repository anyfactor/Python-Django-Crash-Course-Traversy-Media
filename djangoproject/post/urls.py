from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:id>/', views.details, name='details')
]