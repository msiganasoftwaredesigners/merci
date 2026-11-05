from django.contrib.admin import AdminSite as DjangoAdminSite
from django.template.response import TemplateResponse
from django.urls import resolve
from django.http import Http404

class AdminSite(DjangoAdminSite):
    site_header = 'Merci Media Admin'
    site_title = 'Merci Media Admin'

    def each_context(self, request):
        context = super().each_context(request)
        # Always include the Google Analytics link globally in the admin context
        context['google_analytics_link'] = '<a href="https://analytics.google.com/analytics/web/#/p454807736/reports/intelligenthome" target="_blank">Google Analytics</a>'
        return context

    def each_context(self, request):
        context = super().each_context(request)
        context['google_analytics_url'] = 'https://analytics.google.com/analytics/web/#/p454807736/reports/intelligenthome'
        context['google_search_console_url'] = 'https://search.google.com/search-console?resource_id=sc-domain:mercimedia.et'
        return context

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Get the resolved app_label from the request URL
        resolved_url = resolve(request.path_info)
        app_label = resolved_url.kwargs.get('app_label')

        if app_label:
            # If app_label is present in the URL, filter app_list accordingly
            app_list = [app_dict.get(app_label)]
        else:
            # If no app_label present, show all apps
            app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        # Move the 'store' app to the top.
        contact_app = next((app for app in app_list if app['app_label'] == 'contact'), None)
        if contact_app:
            app_list.remove(contact_app)
            app_list.insert(0, contact_app)

        # Move the 'orders' app next to the 'store' app.
        blog_app = next((app for app in app_list if app['app_label'] == 'blog'), None)
        if blog_app:
            app_list.remove(blog_app)
            app_list.insert(1, blog_app)
        
        heads_app = next((app for app in app_list if app['app_label'] == 'heads'), None)
        if blog_app:
            app_list.remove(heads_app)
            app_list.insert(2, heads_app)
        
        footer_app = next((app for app in app_list if app['app_label'] == 'footer'), None)
        if footer_app:
            app_list.remove(footer_app)
            app_list.insert(3, footer_app)

        category_app = next((app for app in app_list if app['app_label'] == 'category'), None)
        if category_app:
            app_list.remove(category_app)
            app_list.insert(4, category_app)

        return app_list

    def app_index(self, request, app_label, extra_context=None):
        app_list = self.get_app_list(request)

        if not app_list:
            raise Http404("The requested admin page does not exist.")

        context = {
            **self.each_context(request),
            "title": f"{app_list[0]['name']} administration",
            "app_list": app_list,
            "app_label": app_label,
        **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(
            request,
            self.app_index_template or ["admin/%s/app_index.html" % app_label, "admin/app_index.html"],
            context,
        )

admin_site = AdminSite(name='admin')
