from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.http import HttpResponsePermanentRedirect


class MerciHostMiddleware:
    """Serve the Merci site at the root of mercimedia.et.

    - mercimedia.et        -> merci.host_urls (home page at "/")
    - www.mercimedia.et    -> 301 redirect to mercimedia.et (one canonical address for SEO)
    - every other host     -> unchanged (msigana.com/merci/ keeps working)

    Add the domains to ALLOWED_HOSTS. Hosts can be changed with MERCI_HOSTS in settings.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        hosts = getattr(settings, "MERCI_HOSTS", ("mercimedia.et", "www.mercimedia.et"))
        self.apex = hosts[0].lower()
        self.hosts = {h.lower() for h in hosts}

    def __call__(self, request):
        try:
            host = request.get_host().split(":")[0].lower()
        except DisallowedHost:
            return self.get_response(request)

        if host in self.hosts:
            if host != self.apex:
                return HttpResponsePermanentRedirect(f"{request.scheme}://{self.apex}{request.get_full_path()}")
            request.urlconf = "merci.host_urls"
        return self.get_response(request)
