from django.contrib import admin
from django.utils.text import slugify
from django.utils.html import strip_tags

from .models import (
    Post,
    Category,
    Business_line,
    BusinessLineGallery,
    BusinessLineService,
)

from msigana_ecommerce.admin_site import admin_site


# -------------------------
# Post
# -------------------------

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    list_display = (
        "title",
        "category",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "short_description",
    )

    list_filter = (
        "category",
        "created_at",
    )

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(strip_tags(obj.title))
        super().save_model(request, obj, form, change)


# -------------------------
# Category
# -------------------------

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    list_display = (
        "name",
        "slug",
    )

    search_fields = (
        "name",
    )


# -------------------------
# Gallery Inline
# -------------------------

class BusinessLineGalleryInline(admin.TabularInline):
    model = BusinessLineGallery
    extra = 1


# -------------------------
# Services Inline
# -------------------------

class BusinessLineServiceInline(admin.TabularInline):
    model = BusinessLineService
    extra = 1


# -------------------------
# Business Line
# -------------------------

class Business_lineAdmin(admin.ModelAdmin):

    prepopulated_fields = {
        "slug": ("name",)
    }

    list_display = (
        "name",
        "Category",
        "views_count",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "Category",
        "created_at",
    )

    readonly_fields = (
        "views_count",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "Category",
                    "slug",
                    "business_services_title",
                    "business_title",
                    "businness_description_title",
                )
            },
        ),
        (
            "Content",
            {
                "fields": (
                    "image",
                    "description",
                )
            },
        ),
        (
            "Website & Registration",
            {
                "fields": (
                    "website_link",
                    "website_link_title",
                    "register_link",
                    "register_link_title",
                )
            },
        ),
        (
            "Statistics",
            {
                "fields": (
                    "views_count",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    inlines = [
        BusinessLineGalleryInline,
        BusinessLineServiceInline,
    ]


# -------------------------
# Register Models
# -------------------------

admin_site.register(Post, PostAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Business_line, Business_lineAdmin)