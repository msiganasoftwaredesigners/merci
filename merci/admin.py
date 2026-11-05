from msigana_ecommerce.admin_site import admin_site

from django.contrib import admin

from .models import MerciInquiry, MerciPhoto, MerciProject, MerciTestimonial


class MerciInquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "organization", "phone", "service", "timeline", "created_at", "handled")
    list_filter = ("service", "language", "handled", "created_at")
    search_fields = ("full_name", "organization", "email", "phone", "project_description")
    list_editable = ("handled",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"


admin_site.register(MerciInquiry, MerciInquiryAdmin)


class MerciProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "youtube_url", "mobile_youtube_url", "is_published", "order")
    list_filter = ("category", "is_published")
    list_editable = ("is_published", "order")
    search_fields = ("title", "description")
    fieldsets = (
        (None, {"fields": ("title", "category", "description", "is_published", "order")}),
        ("Large screen (desktop / tablet)", {"fields": ("youtube_url", "custom_thumbnail")}),
        ("Phone (vertical / short video)", {"fields": ("mobile_youtube_url", "custom_mobile_thumbnail")}),
    )


admin_site.register(MerciProject, MerciProjectAdmin)


class MerciTestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "client_type", "has_video", "is_published", "order")
    list_filter = ("client_type", "is_published")
    list_editable = ("is_published", "order")
    search_fields = ("name", "organization", "quote")

    @admin.display(boolean=True, description="Video")
    def has_video(self, obj):
        return bool(obj.video_id)


admin_site.register(MerciTestimonial, MerciTestimonialAdmin)


class MerciPhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "order", "created_at")
    list_filter = ("category", "is_published")
    list_editable = ("is_published", "order")
    search_fields = ("title", "alt_text")


admin_site.register(MerciPhoto, MerciPhotoAdmin)
