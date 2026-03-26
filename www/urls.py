from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.urls import path
from django.utils.translation import ugettext_lazy as _

admin.autodiscover()

from frontend import views as frontend_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
]

urlpatterns += [
    path('resume.pdf', frontend_views.ResumePdfView.as_view(), name='resume_it'),
    path('resume_en.pdf', frontend_views.ResumeEnPdfView.as_view(), name='resume_en'),
]

pages = [
    path(_('contacts/successful-message-sent/'), frontend_views.thank_you_contact_us, name="_thank_you_contact_us"),
    path(_('contacts/'), frontend_views.contacts, name='contacts'),
    path(_('resume/'), frontend_views.resume, name='resume'),
    path(_('exhibit/<slug:exhibit_slug>'), frontend_views.exhibit_show, name='exhibit_show'),
    path(_('exhibits/'), frontend_views.exhibit_list, name='exhibit_list'),
    path('', frontend_views.homepage, name='homepage'),
]

urlpatterns += i18n_patterns(
    path(_(''), include(pages)),
    prefix_default_language=False,
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

