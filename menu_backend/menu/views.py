"""
Vistas (Views) para la API REST
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Categoria, ItemMenu
from django.db import models
from .serializers import MenuCompletoSerializer, CategoriaSerializer, ItemMenuSerializer

@api_view(['GET'])
def menu_completo(request):
    """
    Endpoint: GET /api/menu/
    Descripción: Retorna el menú completo con categorías e ítems
    """
    serializer = MenuCompletoSerializer(
        {}, 
        context={'request': request}
    )
    return Response(serializer.data)


class CategoriaListView(generics.ListAPIView):
    """
    Endpoint: GET /api/menu/categories/
    Descripción: Lista todas las categorías activas
    """
    queryset = Categoria.objects.filter(is_active=True).order_by('orden')
    serializer_class = CategoriaSerializer


class ItemMenuListView(generics.ListAPIView):
    """
    Endpoint: GET /api/menu/items/
    Descripción: Lista ítems con filtros opcionales
    """
    serializer_class = ItemMenuSerializer

    def get_queryset(self):
        queryset = ItemMenu.objects.filter(is_active=True)
        
        # Filtro por categoría
        categoria = self.request.query_params.get('category', None)
        if categoria:
            queryset = queryset.filter(categoria__nombre__icontains=categoria)
        
        # Filtro por badge
        badge = self.request.query_params.get('badge', None)
        if badge:
            queryset = queryset.filter(badges=badge)
        
        # Búsqueda por nombre o descripción
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(nombre__icontains=search) | 
                models.Q(descripcion__icontains=search)
            )
        
        return queryset.order_by('categoria__orden', 'nombre')


class ItemMenuDetailView(generics.RetrieveAPIView):
    """
    Endpoint: GET /api/menu/items/{id}/
    Descripción: Obtiene un ítem específico por ID
    """
    queryset = ItemMenu.objects.filter(is_active=True)
    serializer_class = ItemMenuSerializer