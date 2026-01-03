""" menu/urls,py
URLs para la API de Menu
"""
from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_completo, name='menu-completo'),
    path('menu/categories/', views.CategoriaListView.as_view(), name='categoria-list'),
    path('menu/items/', views.ItemMenuListView.as_view(), name='item-list'),
]
