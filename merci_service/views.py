import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import MerciInquiryForm
from .models import MerciProject

logger = logging.getLogger(__name__)

SERVICES = [
    {"icon": "video", "title": "Professional Video Production", "items": [
        "Corporate and company profile videos", "Promotional and advertising videos",
        "Brand storytelling and campaign videos", "Event coverage and highlight videos",
        "Educational and training videos", "Social media videos, reels, and short-form content",
        "Interviews and testimonial videos"]},
    {"icon": "camera", "title": "Professional Photography", "items": [
        "Corporate and business photography", "Product and commercial photography",
        "Portrait and professional profile photography", "Event and conference photography",
        "Documentary photography", "Brand and marketing photography"]},
    {"icon": "mic", "title": "Studio Production", "intro": "Planned, controlled production in a studio setting.", "items": [
        "Studio-based video recording", "Interviews and professional presentations",
        "Educational and training content", "Talk shows and discussion programs",
        "Presenter-led videos", "Product and promotional shoots", "Audio and visual content recording"]},
    {"icon": "film", "title": "Documentary Production", "intro": "One of our key services, from research to delivery.", "items": [
        "Corporate and institutional documentaries", "Social impact and development documentaries",
        "Cultural and community documentaries", "NGO and project documentaries",
        "Human-interest and personal stories", "Research, field interviews, and location filming",
        "Documentary scripting, filming, editing, and delivery"]},
    {"icon": "globe", "title": "Multilingual Content Production", "intro": "Content for audiences in Ethiopia and abroad.", "items": [
        "Content in local Ethiopian languages", "Content in foreign languages",
        "Multilingual interviews and presentations", "Educational and instructional videos",
        "Language-learning content", "Script preparation and localization coordination",
        "Subtitles and multilingual versions, depending on project requirements"]},
    {"icon": "user", "title": "Video Hosting and Presentation", "intro": "We provide or coordinate hosts and presenters to match your project's language, audience, and requirements.", "items": [
        "Professional video hosts and presenters", "Interview hosts and moderators",
        "Educational video presenters", "Promotional video presenters",
        "Presenter-led business and institutional content", "Host coordination and production support"]},
]

STEPS = [
    ("Discovery and Consultation", "We understand your goals, audience, message, budget, and expected outcomes."),
    ("Concept and Pre-Production", "We develop the concept, creative direction, scripts, production plan, locations, and schedule."),
    ("Content and Production Planning", "We coordinate equipment, studio arrangements, presenters, crew, and other production requirements."),
    ("Filming and Photography", "We capture professional video and photography in our studio or at your preferred location."),
    ("Post-Production", "We handle editing, audio refinement, color correction, graphics, titles, subtitles, and other agreed requirements."),
    ("Review and Final Delivery", "We coordinate your feedback, complete revisions within the agreed scope, and deliver approved content in suitable formats."),
]

CLIENTS = [
    "Businesses and private companies", "Government institutions",
    "NGOs and international development organizations",
    "Educational institutions and training providers",
    "Tourism and cultural organizations",
    "Corporate communication and marketing teams",
    "Entrepreneurs, professionals, and personal brands",
]

BENEFITS = [
    ("layers", "End-to-End Production", "One coordinated team from concept to delivery."),
    ("camera", "Studio and On-Location", "Production planning for different environments."),
    ("globe", "Multilingual Content", "Content designed for local and international audiences."),
    ("spark", "Creative Storytelling", "Visual content that communicates a clear message."),
    ("bolt", "Flexible Services", "Individual services or complete production packages."),
    ("building", "Technology-Enabled Delivery", "Backed by the broader capabilities of Misgana Technologies PLC."),
]



def merci_home(request):
    if request.method == "POST":
        form = MerciInquiryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get("website"):  # honeypot tripped
                return redirect(f"{reverse('merci:home')}?sent=1#inquiry")
            inquiry = form.save()
            try:
                send_mail(
                    subject=f"New Merci inquiry: {inquiry.get_service_display()} from {inquiry.full_name}",
                    message=(
                        f"Name: {inquiry.full_name}\nOrganization: {inquiry.organization}\n"
                        f"Email: {inquiry.email}\nPhone: {inquiry.phone}\n"
                        f"Service: {inquiry.get_service_display()}\n"
                        f"Language: {inquiry.get_language_display()}\n"
                        f"Timeline: {inquiry.get_timeline_display()}\nBudget: {inquiry.budget}\n\n"
                        f"{inquiry.project_description}"
                    ),
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=[getattr(settings, "MERCI_INQUIRY_EMAIL", settings.DEFAULT_FROM_EMAIL)],
                    fail_silently=False,
                )
            except Exception:  # the inquiry is already saved; don't fail the visitor
                logger.exception("Could not send Merci inquiry email")
            return redirect(f"{reverse('merci:home')}?sent=1#inquiry")
    else:
        form = MerciInquiryForm(initial={"service": request.GET.get("service", "")})

    return render(request, "merci/merci.html", {
        "form": form,
        "sent": request.GET.get("sent") == "1",
        "services": SERVICES,
        "steps": STEPS,
        "clients": CLIENTS,
        "benefits": BENEFITS,
        "portfolio_categories": MerciProject.CATEGORY_CHOICES,
        "projects": MerciProject.objects.filter(is_published=True),
        "youtube_channel_url": getattr(settings, "MERCI_YOUTUBE_CHANNEL_URL", ""),
    })