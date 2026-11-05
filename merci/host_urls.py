"""URLconf used when the site is opened as mercimedia.et (or www.mercimedia.et).

The whole project now serves Merci from the root URLconf, so this simply reuses it.
merci.middleware.MerciHostMiddleware still redirects www.mercimedia.et to mercimedia.et.
"""
from msigana_ecommerce.urls import urlpatterns  # noqa: F401
