from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

admin.autodiscover()

from frontend import views as frontend_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', frontend_views.layout_preview_one, name='homepage'),
    path('bozza-1/', frontend_views.layout_preview_one, name='layout_preview_one'),
    path('bozza-2/', frontend_views.layout_preview_two, name='layout_preview_two'),
    path('bozza-3/', frontend_views.layout_preview_three, name='layout_preview_three'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
