from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# Importa TU admin personalizado, no el de Django
from .admin import admin_site

def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>QuickMenu API</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: #333; }
            .links { margin-top: 30px; }
            .link-btn { 
                display: inline-block; 
                margin: 10px; 
                padding: 15px 30px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                text-decoration: none; 
                border-radius: 8px;
                font-weight: bold;
                transition: transform 0.2s;
            }
            .link-btn:hover { 
                transform: translateY(-2px); 
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 QuickMenu API</h1>
            <p>Backend para el sistema de menú digital del restaurante</p>
            
            <div class="links">
                <a href="/admin/" class="link-btn">📊 Panel de Administración</a>
                <a href="/api/menu/" class="link-btn">📋 Ver Menú (API)</a>
                <a href="/api/menu/categories/" class="link-btn">📂 Ver Categorías</a>
                <a href="/api/menu/items/" class="link-btn">🍕 Ver Ítems</a>
            </div>
            
            <div style="margin-top: 50px; color: #666;">
                <p>Endpoints disponibles:</p>
                <code>/api/menu/</code> - Menú completo<br>
                <code>/api/menu/categories/</code> - Categorías<br>
                <code>/api/menu/items/</code> - Ítems del menú
            </div>
        </div>
    </body>
    </html>
    """)

# Usa admin_site (tu admin personalizado) en lugar de admin.site
urlpatterns = [
    path('admin/', admin_site.urls),  # ← IMPORTANTE: admin_site, no admin.site
    path('api/', include('menu_backend.menu.urls')),
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)