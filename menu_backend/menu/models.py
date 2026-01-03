"""
Modelos de datos para la aplicación Menu
"""
from django.db import models

class Categoria(models.Model):
    """
    Modelo para categorías del menú (Entradas, Platos Fuertes, Postres, etc.)
    """
    nombre = models.CharField(max_length=100, unique=True)
    orden = models.PositiveIntegerField(default=0, help_text="Orden de visualización")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre

    @property
    def item_count(self):
        """Retorna la cantidad de ítems activos en esta categoría"""
        return self.items.filter(is_active=True).count()


class ItemMenu(models.Model):
    """
    Modelo para los ítems del menú (platos, bebidas, etc.)
    """
    # Opciones para los badges (etiquetas)
    BADGE_OPCIONES = [
        ('recomendado', '⭐ Recomendado'),
        ('Desayunos', ' Desayunos'),
        ('Almuerzos', ' Almuerzos'),
        ('Especiales', 'Especiales'),
        ('Escurcion', 'Escurcion'),
    ]

    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Campos adicionales basados en la documentación del frontend
    ingredients = models.TextField(
        blank=True, 
        help_text="Ingredientes separados por comas o saltos de línea"
    )
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=4.5,
        help_text="Calificación de 1.0 a 5.0"
    )
    preparation_time = models.CharField(
        max_length=50, 
        blank=True, 
        default="15-20 min"
    )
    portions = models.CharField(
        max_length=50, 
        blank=True, 
        default="1 persona"
    )
    
    # Badges como CharField con opciones (puede estar vacío)
    badges = models.CharField(
        max_length=50, 
        choices=BADGE_OPCIONES, 
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ítem del Menú"
        verbose_name_plural = "Ítems del Menú"
        ordering = ['categoria__orden', 'nombre']

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    def get_ingredients_list(self):
        """Convierte el texto de ingredientes en una lista"""
        if self.ingredients:
            # Divide por comas o saltos de línea y limpia espacios
            return [ing.strip() for ing in self.ingredients.replace('\n', ',').split(',') if ing.strip()]
        return []


class ItemImage(models.Model):
    """
    Modelo para manejar múltiples imágenes por ítem del menú
    """
    item = models.ForeignKey(
        ItemMenu, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(
        upload_to='menu_images/%Y/%m/%d/',
        help_text="Formatos: JPEG, PNG, WebP. Tamaño máximo: 2MB"
    )
    orden = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen del Ítem"
        verbose_name_plural = "Imágenes del Ítem"
        ordering = ['orden']

    def __str__(self):
        return f"Imagen de {self.item.nombre}"