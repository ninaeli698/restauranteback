"""
Personalización GLOBAL del Admin Site para QuickMenu
"""
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
import datetime

class CustomAdminSite(AdminSite):
    """
    Admin Site personalizado con mejoras visuales y funcionales
    """
    # Textos que aparecen en todo el admin
    site_header = "🍽️ QuickMenu - Panel de Administración"
    site_title = "QuickMenu Admin Dashboard"
    index_title = "📊 Gestión del Menú Digital"
    
    # URLs personalizadas
    site_url = "/"
    
    def each_context(self, request):
        """
        Agrega contexto adicional a todas las páginas del admin
        """
        context = super().each_context(request)
        
        # Agregar estadísticas básicas
        try:
            from menu.models import Categoria, ItemMenu
            context['total_categorias'] = Categoria.objects.count()
            context['total_items'] = ItemMenu.objects.count()
            context['items_activos'] = ItemMenu.objects.filter(is_active=True).count()
            context['hoy'] = datetime.date.today().strftime("%d/%m/%Y")
        except:
            pass
            
        return context
    
    def get_app_list(self, request, app_label=None):
        """
        Personaliza el orden y aspecto de las apps en el sidebar
        """
        app_list = super().get_app_list(request, app_label)
        
        # Diccionario de iconos para cada app
        app_icons = {
            'menu': '🍽️',
            'auth': '👥',
            'sessions': '💻',
        }
        
        # Agregar iconos y personalizar nombres
        for app in app_list:
            app_name = app['name'].lower()
            
            # Agregar icono
            icon = app_icons.get(app_name, '📁')
            app['name'] = f"{icon} {app['name']}"
            
            # Personalizar nombres de modelos específicos
            for model in app['models']:
                if model['object_name'] == 'Categoria':
                    model['name'] = f"📂 {model['name']}"
                elif model['object_name'] == 'ItemMenu':
                    model['name'] = f"🍕 {model['name']}"
                elif model['object_name'] == 'ItemImage':
                    model['name'] = f"🖼️ {model['name']}"
                elif model['object_name'] == 'User':
                    model['name'] = f"👤 {model['name']}"
                elif model['object_name'] == 'Group':
                    model['name'] = f"👥 {model['name']}"
        
        return app_list

# Instancia global del admin personalizado
admin_site = CustomAdminSite(name='custom_admin')