"""Root URLs: the whole site is Merci Media & Digitals.

    /                   home page
    /<service-slug>/    service landing pages (see merci/views.py LANDING)
    /services/          all services
    /blog/, /blog/<slug>/   articles (managed in /admin/ under Blog > Posts)
    /robots.txt, /sitemap.xml
    /admin/             manage projects, photos, testimonials and enquiries
    /merci/             permanent redirect to / (old address)

The previous Msigana routes are archived in legacy_msigana_urls.py.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView

from merci import views as merci_views

from .admin_site import admin_site

urlpatterns = [
    path("admin/", admin_site.urls),
    path("robots.txt", merci_views.robots_txt, name="robots"),
    path("sitemap.xml", merci_views.sitemap_xml, name="sitemap"),
    path("merci/", RedirectView.as_view(url="/", permanent=True)),
    path("video-production/", include("merci_service.urls")),
    path("blog/", include("blog.urls")),
    path("news/", RedirectView.as_view(url="/blog/", permanent=True)),  # old Msigana address
    path("news/<slug:slug>/", RedirectView.as_view(pattern_name="blog:detail", permanent=True)),
    path("", include("merci.urls")),
]

if settings.DEBUG:
    if "django_browser_reload" in settings.INSTALLED_APPS:
        urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
