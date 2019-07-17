# dashboard/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('dashboard_view/', views.dashboard_view, name='dashboard_view'),
    # path('geo_view/', views.geo_view, name='geo_view'),
    path('tasks/', views.tasks, name='tasks'),
    path('site_based/', views.geo_site_based, name='site_based'),
    path('grid_based/', views.geo_grid_based, name='grid_based'),
    path('geo_grid_coverage/', views.geo_grid_coverage, name='geo_grid_coverage'),
]
