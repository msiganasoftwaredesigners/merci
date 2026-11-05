import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


YOUTUBE_ID_RE = re.compile(
    r"(?:youtu\.be/|youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/|live/|v/))([A-Za-z0-9_-]{11})"
)


class MerciInquiry(models.Model):
    SERVICE_CHOICES = [
        ("video", "Video production"),
        ("retainer", "Monthly content package"),
        ("ngo", "NGO documentary or campaign"),
        ("event", "Birthday, wedding or private event"),
        ("photography", "Photography"),
        ("studio", "Studio production"),
        ("documentary", "Documentary production"),
        ("multilingual", "Multilingual content"),
        ("hosting", "Video hosting and presentation"),
        ("package", "Complete production package"),
    ]
    LANGUAGE_CHOICES = [
        ("amharic", "Amharic"),
        ("oromo", "Afaan Oromoo"),
        ("tigrinya", "Tigrinya"),
        ("somali", "Somali"),
        ("afar", "Afar"),
        ("english", "English"),
        ("french", "French"),
        ("arabic", "Arabic"),
        ("other", "Other (tell us in the description)"),
    ]
    TIMELINE_CHOICES = [
        ("asap", "As soon as possible"),
        ("2_weeks", "Within 2 weeks"),
        ("1_month", "Within 1 month"),
        ("1_3_months", "1 to 3 months"),
        ("flexible", "Flexible"),
    ]

    phone_validator = RegexValidator(
        r"^\+?[0-9\s\-()]{7,20}$", "Enter a valid phone number, e.g. +251 9XX XXX XXX."
    )

    # Only name, phone, service and a short description are required, so enquiring takes under a minute.
    full_name = models.CharField(max_length=120)
    organization = models.CharField("Company or organization", max_length=160, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=25, validators=[phone_validator])
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    language = models.CharField("Preferred production language", max_length=20, choices=LANGUAGE_CHOICES, blank=True)
    project_description = models.TextField()
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES, blank=True)
    budget = models.CharField("Estimated budget (optional)", max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Merci inquiry"
        verbose_name_plural = "Merci inquiries"

    def __str__(self):
        return f"{self.full_name} - {self.get_service_display()}"


class MerciProject(models.Model):
    """A portfolio item. The video lives on YouTube; we only store its link."""

    CATEGORY_CHOICES = [
        ("corporate", "Corporate Videos"),
        ("documentary", "Documentaries"),
        ("studio", "Studio Productions"),
        ("commercial", "Commercial and Promotional Videos"),
        ("events", "Event Photography and Videography"),
        ("educational", "Educational and Multilingual Content"),
    ]

    title = models.CharField(max_length=160)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=300, blank=True)

    # Large-screen video
    youtube_url = models.URLField(
        "YouTube link (desktop / large screen)",
        help_text="Paste the YouTube link, e.g. https://www.youtube.com/watch?v=XXXXXXXXXXX or https://youtu.be/XXXXXXXXXXX",
    )
    custom_thumbnail = models.ImageField(
        upload_to="merci/thumbnails/", blank=True,
        help_text="Optional. Leave empty to use the YouTube thumbnail (saves server space).",
    )

    # Phone-size (vertical) video
    mobile_youtube_url = models.URLField(
        "YouTube link (mobile / short video)", blank=True,
        help_text="Optional. Paste a vertical video or YouTube Shorts link, e.g. https://www.youtube.com/shorts/XXXXXXXXXXX. If empty, phones will use the desktop video.",
    )
    custom_mobile_thumbnail = models.ImageField(
        upload_to="merci/thumbnails/", blank=True,
        help_text="Optional. Vertical thumbnail for phones. Leave empty to use the YouTube thumbnail.",
    )

    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Merci project"
        verbose_name_plural = "Merci projects"

    def __str__(self):
        return self.title

    # ---- desktop ----
    @property
    def video_id(self):
        match = YOUTUBE_ID_RE.search(self.youtube_url or "")
        return match.group(1) if match else ""

    @property
    def thumbnail_url(self):
        if self.custom_thumbnail:
            return self.custom_thumbnail.url
        return f"https://i.ytimg.com/vi/{self.video_id}/hqdefault.jpg"

    @property
    def embed_url(self):
        return f"https://www.youtube-nocookie.com/embed/{self.video_id}?autoplay=1&rel=0&modestbranding=1&playsinline=1"

    # ---- mobile ----
    @property
    def has_mobile_video(self):
        return bool(YOUTUBE_ID_RE.search(self.mobile_youtube_url or ""))

    @property
    def mobile_video_id(self):
        match = YOUTUBE_ID_RE.search(self.mobile_youtube_url or "")
        return match.group(1) if match else self.video_id  # fall back to the desktop video

    @property
    def mobile_thumbnail_url(self):
        if self.custom_mobile_thumbnail:
            return self.custom_mobile_thumbnail.url
        if self.has_mobile_video:
            return f"https://i.ytimg.com/vi/{self.mobile_video_id}/hqdefault.jpg"
        return self.thumbnail_url

    @property
    def mobile_embed_url(self):
        return f"https://www.youtube-nocookie.com/embed/{self.mobile_video_id}?autoplay=1&rel=0&modestbranding=1&playsinline=1"

    def clean(self):
        if not self.video_id:
            raise ValidationError({"youtube_url": "Enter a valid YouTube video link."})
        if self.mobile_youtube_url and not YOUTUBE_ID_RE.search(self.mobile_youtube_url):
            raise ValidationError({"mobile_youtube_url": "Enter a valid YouTube video or Shorts link."})


class MerciTestimonial(models.Model):
    """A client testimonial. Written quote, optional portrait/logo, optional YouTube video."""

    CLIENT_TYPE_CHOICES = [
        ("company", "Company"),
        ("ngo", "NGO / institution"),
        ("individual", "Individual / personal brand"),
    ]

    name = models.CharField(max_length=120)
    role = models.CharField("Role or job title", max_length=120, blank=True)
    organization = models.CharField(max_length=160, blank=True)
    client_type = models.CharField(max_length=12, choices=CLIENT_TYPE_CHOICES, default="company")
    quote = models.TextField(help_text="What the client said, in their own words. Keep it under about 400 characters.")
    photo = models.ImageField(
        upload_to="merci/testimonials/", blank=True,
        help_text="Optional. A square portrait or the client logo.",
    )
    video_url = models.URLField(
        "YouTube link (video testimonial)", blank=True,
        help_text="Optional. If added, visitors can play the client's video testimonial.",
    )
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Merci testimonial"
        verbose_name_plural = "Merci testimonials"

    def __str__(self):
        return f"{self.name} ({self.organization})" if self.organization else self.name

    @property
    def video_id(self):
        match = YOUTUBE_ID_RE.search(self.video_url or "")
        return match.group(1) if match else ""

    @property
    def video_thumbnail_url(self):
        return f"https://i.ytimg.com/vi/{self.video_id}/hqdefault.jpg" if self.video_id else ""

    @property
    def embed_url(self):
        return f"https://www.youtube-nocookie.com/embed/{self.video_id}?autoplay=1&rel=0&modestbranding=1&playsinline=1" if self.video_id else ""

    @property
    def initials(self):
        parts = [p for p in self.name.split() if p]
        return "".join(p[0] for p in parts[:2]).upper() or "M"

    def clean(self):
        if self.video_url and not self.video_id:
            raise ValidationError({"video_url": "Enter a valid YouTube video link."})


class MerciPhoto(models.Model):
    """A portfolio photograph shown in the photo gallery."""

    CATEGORY_CHOICES = [
        ("corporate", "Corporate"),
        ("portrait", "Portraits"),
        ("product", "Product"),
        ("event", "Events"),
        ("documentary", "Documentary"),
        ("behind", "Behind the scenes"),
    ]

    title = models.CharField(max_length=160)
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, default="corporate")
    image = models.ImageField(
        upload_to="merci/photos/",
        help_text="Landscape or portrait both work. Keep the file under 1 MB (about 1600 px on the long side) so the page stays fast.",
    )
    alt_text = models.CharField(
        max_length=200, blank=True,
        help_text="Describe the photo in a few words. Helps Google Images and screen readers. Defaults to the title.",
    )
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Merci photo"
        verbose_name_plural = "Merci photos"

    def __str__(self):
        return self.title

    @property
    def alt(self):
        return self.alt_text or self.title
