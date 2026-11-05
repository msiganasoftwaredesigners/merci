from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import MerciInquiry, MerciProject, MerciTestimonial

VALID = {
    "full_name": "Test Client",
    "phone": "+251 911 000 000",
    "service": "video",
    "project_description": "We need a 60 second company video.",
}


@override_settings(DEFAULT_FROM_EMAIL="noreply@example.com", MERCI_INQUIRY_EMAIL="team@example.com")
class MerciPageTests(TestCase):
    def test_home_page_loads_with_core_content(self):
        response = self.client.get(reverse("merci:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Stories that make people")
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, "application/ld+json")

    def test_only_four_fields_are_required(self):
        response = self.client.post(reverse("merci:home"), VALID)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MerciInquiry.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_invalid_phone_shows_error_and_saves_nothing(self):
        response = self.client.post(reverse("merci:home"), {**VALID, "phone": "abc"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "valid phone number")
        self.assertEqual(MerciInquiry.objects.count(), 0)

    def test_honeypot_discards_bot_submissions(self):
        response = self.client.post(reverse("merci:home"), {**VALID, "website": "http://spam.example"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MerciInquiry.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_published_project_and_testimonial_are_shown(self):
        MerciProject.objects.create(title="Test Film", category="corporate", youtube_url="https://youtu.be/abcdefghijk")
        MerciTestimonial.objects.create(name="Selam", quote="Great work from the whole team.")
        response = self.client.get(reverse("merci:home"))
        self.assertContains(response, "Test Film")
        self.assertContains(response, "Great work from the whole team.")


class MerciSeoAndLandingTests(TestCase):
    def test_every_landing_page_loads_with_its_own_title(self):
        from .views import LANDING
        for slug, page in LANDING.items():
            response = self.client.get(reverse("merci:landing", args=[slug]))
            self.assertEqual(response.status_code, 200, slug)
            self.assertContains(response, page["h1"])
            self.assertContains(response, "application/ld+json")

    def test_unknown_landing_page_is_404(self):
        self.assertEqual(self.client.get("/not-a-page/").status_code, 404)

    def test_sitemap_lists_home_and_landing_pages(self):
        from .views import LANDING
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        for slug in LANDING:
            self.assertContains(response, f"/{slug}/")

    def test_robots_points_to_sitemap(self):
        self.assertContains(self.client.get("/robots.txt"), "Sitemap:")

    def test_old_merci_address_redirects_to_root(self):
        response = self.client.get("/merci/")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/")


class ServicesAndBlogTests(TestCase):
    def test_services_page_lists_every_service(self):
        from .views import SERVICES
        response = self.client.get(reverse("merci:services"))
        self.assertEqual(response.status_code, 200)
        for service in SERVICES:
            self.assertContains(response, service["title"])
        self.assertContains(response, "application/ld+json")

    def test_services_page_accepts_a_quote_request(self):
        response = self.client.post(reverse("merci:services"), VALID)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["Location"].startswith("/services/?sent=1"))
        self.assertEqual(MerciInquiry.objects.count(), 1)

    def test_blog_list_loads_even_with_no_posts(self):
        response = self.client.get(reverse("blog:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Articles are on the way")

    def test_unknown_blog_post_is_404(self):
        self.assertEqual(self.client.get("/blog/does-not-exist/").status_code, 404)

    def test_old_news_addresses_redirect_to_blog(self):
        self.assertEqual(self.client.get("/news/").status_code, 301)
        self.assertEqual(self.client.get("/news/some-post/")["Location"], "/blog/some-post/")

    def test_sitemap_includes_services_and_blog(self):
        response = self.client.get("/sitemap.xml")
        self.assertContains(response, "/services/")
        self.assertContains(response, "/blog/")
