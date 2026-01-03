"""
Serializers para convertir modelos Django a JSON para la API
"""
from rest_framework import serializers
from .models import Categoria, ItemMenu, ItemImage

class ItemImageSerializer(serializers.ModelSerializer):
    """
    Serializer para las imágenes de los ítems
    """
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ItemImage
        fields = ['image_url', 'orden']

    def get_image_url(self, obj):
        """Retorna la URL completa de la imagen"""
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None


class ItemMenuSerializer(serializers.ModelSerializer):
    """
    Serializer para los ítems del menú
    """
    images = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = ItemMenu
        fields = [
            'id',
            'nombre',
            'descripcion', 
            'precio',
            'images',
            'badges',
            'ingredients',
            'rating',
            'preparation_time',
            'portions'
        ]

    def get_images(self, obj):
        """Obtiene todas las imágenes del ítem ordenadas"""
        images = obj.images.all().order_by('orden')
        return ItemImageSerializer(
            images, 
            many=True, 
            context={'request': self.context.get('request')}
        ).data

    def get_ingredients(self, obj):
        """Convierte el texto de ingredientes en una lista"""
        return obj.get_ingredients_list()


class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializer para las categorías con sus ítems
    """
    items = serializers.SerializerMethodField()
    item_count = serializers.ReadOnlyField()

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'items', 'item_count']

    def get_name(self, obj):
        """Asegura que el campo se llame 'name' en el JSON"""
        return obj.nombre

    def get_items(self, obj):
        """Obtiene solo los ítems activos de la categoría"""
        active_items = obj.items.filter(is_active=True).order_by('nombre')
        return ItemMenuSerializer(
            active_items, 
            many=True, 
            context={'request': self.context.get('request')}
        ).data


class MenuCompletoSerializer(serializers.Serializer):
    """
    Serializer para la respuesta completa del menú
    """
    restaurantName = serializers.CharField(default="Sabores del Mundo")
    categories = serializers.SerializerMethodField()

    def get_categories(self, obj):
        """Obtiene todas las categorías activas con sus ítems"""
        active_categories = Categoria.objects.filter(is_active=True).order_by('orden')
        return CategoriaSerializer(
            active_categories,
            many=True,
            context={'request': self.context.get('request')}
        ).data