from django.contrib import admin
from django.utils.html import format_html
from menu_backend.admin import admin_site  # ← Importa TU admin personalizado
from .models import Categoria, ItemMenu, ItemImage

# ========== REGISTRA TUS MODELOS CON admin_site (no con admin) ==========

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    fields = ('image', 'image_preview', 'orden')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 6px;" />',
                obj.image.url
            )
        return "📷"
    image_preview.short_description = "Vista previa"

@admin.register(Categoria, site=admin_site)  # ← Registra con admin_site
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'item_count', 'is_active_display', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('nombre',)
    list_per_page = 20
    
    def item_count(self, obj):
        count = obj.items.count()
        color = "#28a745" if count > 0 else "#ffc107"
        return format_html(
            '<span style="color: {}; font-weight: bold; background: #f8f9fa; padding: 3px 8px; border-radius: 12px;">{} ítems</span>',
            color, count
        )
    item_count.short_description = "Total Ítems"
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">● Activa</span>'
            )
        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">○ Inactiva</span>'
        )
    is_active_display.short_description = "Estado"

@admin.register(ItemMenu, site=admin_site)  # ← Registra con admin_site
class ItemMenuAdmin(admin.ModelAdmin):
    list_display = (
        'image_preview',
        'nombre', 
        'categoria',
        'precio',
        'badges',
        'rating_display',
        'is_active_display'
    )
    
    list_filter = ('categoria', 'badges', 'is_active')
    search_fields = ('nombre', 'descripcion', 'ingredients')
    list_per_page = 25
    list_editable = ('precio', 'badges')
    inlines = [ItemImageInline]
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('categoria', 'nombre', 'descripcion', 'precio', 'badges'),
            'classes': ('wide',),
        }),
        ('Detalles Adicionales', {
            'fields': ('ingredients', 'rating', 'preparation_time', 'portions', 'is_active'),
            'classes': ('collapse',),
        }),
    )
    
    def image_preview(self, obj):
        first_image = obj.images.first()
        if first_image and first_image.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 6px;" />',
                first_image.image.url
            )
        return "📷"
    image_preview.short_description = "Imagen"
    
    def precio_formateado(self, obj):
        return format_html(
            '<span style="color: #28a745; font-weight: bold;">${:,.0f}</span>',
            obj.precio
        )
    precio_formateado.short_description = "Precio"
    
    def badges_display(self, obj):
        if obj.badges:
            badge_icons = {
                'recomendado': '⭐',
                'vegano': '🌱',
                'vegetariano': '🥕',
                'sin-gluten': '🍞',
                'picante': '🌶️',
            }
            icon = badge_icons.get(obj.badges, '🏷️')
            return format_html(
                '<span style="background: #e9ecef; padding: 3px 10px; border-radius: 15px; font-size: 12px;">{} {}</span>',
                icon, obj.get_badges_display()
            )
        return "-"
    badges_display.short_description = "Etiqueta"
    
    def rating_display(self, obj):
        stars = "★" * int(obj.rating) + "☆" * (5 - int(obj.rating))
        return format_html(
            '<span style="color: #ffc107; font-weight: bold;">{} {}/5</span>',
            stars, obj.rating
        )
    rating_display.short_description = "Rating"
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✓ Activo</span>'
            )
        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">✗ Inactivo</span>'
        )
    is_active_display.short_description = "Estado"

@admin.register(ItemImage, site=admin_site)  # ← Registra con admin_site
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'image_preview', 'orden')
    list_filter = ('created_at',)
    search_fields = ('item__nombre',)
    list_editable = ('orden',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "📷"
    image_preview.short_description = "Vista previa"