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
    path('resume.pdf', frontend_views.ResumePdfView.as_view(), name='resume_it'),
    path('resume_en.pdf', frontend_views.ResumeEnPdfView.as_view(), name='resume_en'),
    path('contacts/successful-message-sent/', frontend_views.thank_you_contact_us, name="_thank_you_contact_us"),
    path('contacts/', frontend_views.contacts, name='contacts'),
    path('resume/', frontend_views.resume, name='resume'),
    path('exhibit/<slug:exhibit_slug>', frontend_views.exhibit_show, name='exhibit_show'),
    path('exhibits/', frontend_views.exhibit_list, name='exhibit_list'),
    path('', frontend_views.homepage, name='homepage'),
    path('bozza-1/', frontend_views.layout_preview_one, name='layout_preview_one'),
    path('bozza-2/', frontend_views.layout_preview_two, name='layout_preview_two'),
    path('bozza-3/', frontend_views.layout_preview_three, name='layout_preview_three'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
