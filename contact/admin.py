from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage
from msigana_ecommerce.admin_site import admin_site

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    ordering = ('-created_at',)

    def email_login_link(self, obj=None):
        return format_html(
            '<a href="{}" target="_blank" style="color: green; font-weight: bold;">Email Login</a>',
            'https://s1478.lon1.mysecurecloudhost.com:2096/'
        )
    email_login_link.short_description = 'Email Login'  # Display name in admin

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['email_login_link'] = self.email_login_link()  # Pass the link to template context
        return super().changelist_view(request, extra_context=extra_context)

    # Optionally, add the link to the admin page as a readonly field
    readonly_fields = ('email_login_link',)

admin_site.register(ContactMessage, ContactMessageAdmin)
