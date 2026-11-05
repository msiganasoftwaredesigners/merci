# ARCHIVE ONLY: the original Msigana routes, kept for reference. Not used (ROOT_URLCONF is msigana_ecommerce.urls, which now serves Merci).
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from msigana_ecommerce.admin_site import admin_site
from django.views.generic import TemplateView
from django.contrib.staticfiles.views import serve

# from django.contrib import admin

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', views.home, name='home'),
    path(
    'business-line/<slug:slug>/',
    views.business_line_detail,
    name='business_line_detail'
),
    path('services', views.services, name='services'),
    path('news/', include('blog.urls')),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('about-us/', views.about_us, name='about-us'),
    path('contact-us/', include('contact.urls')),
    path('customers/', include('customers.urls')),
    path('accounts/', include('allauth.urls')),
    path("accounts/profile/", views.update_profile, name="users_profiles"),  
    path('merci/', include('merci.urls')),
    path('send-text/', include('send_text.urls')),
    path(
    "business_line/<slug:slug>/",
    views.service_detail,
    name="service_detail"
),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml")),
]


if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
