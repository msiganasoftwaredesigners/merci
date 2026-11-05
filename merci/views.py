import json
import logging
from urllib.parse import quote

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET

from .forms import MerciInquiryForm, OPTIONAL_FIELDS
from .models import MerciInquiry, MerciPhoto, MerciProject, MerciTestimonial

logger = logging.getLogger(__name__)

BRAND = "Merci Media & Digitals"

# ---------------------------------------------------------------------------
# Contact details and links. Override any of these in settings.py with
#     MERCI_SITE = {"phone": "+251...", "email": "hello@mercimedia.et", ...}
# or leave a value empty to hide it from the page.
# ---------------------------------------------------------------------------
DEFAULT_SITE = {
    "url": "https://mercimedia.et",
    "phone": "+251995030727",
    "phone_display": "+251 99 503 0727",
    "whatsapp": "251995030727",
    "email": "info@mercimedia.et",
    "telegram": "",
    "address": "Ras Abebe Aragay St, Addis Ababa, Ethiopia",
    "youtube": "",
    "instagram": "",
    "tiktok": "",
    "linkedin": "",
    "facebook": "",
    "parent_url": "https://mercimedia.et",
    "ga_id": "",
}

WHATSAPP_GREETING = "Hello Merci Media, I would like a quote for a video project."


def get_site():
    site = {**DEFAULT_SITE, **getattr(settings, "MERCI_SITE", {})}
    site["url"] = site["url"].rstrip("/")
    digits = "".join(ch for ch in site["whatsapp"] if ch.isdigit())
    site["whatsapp_digits"] = digits
    site["whatsapp_url"] = f"https://wa.me/{digits}?text={quote(WHATSAPP_GREETING)}" if digits else ""
    return site


# ---------------------------------------------------------------------------
# Page content. Edit the text here; no template changes needed.
# `key` on a service or package pre-selects that option in the enquiry form.
# ---------------------------------------------------------------------------
SERVICES = [
    {"key": "video", "icon": "video", "page": "corporate-video-production-addis-ababa",
     "title": "Corporate and Brand Videos",
     "blurb": "Company films, adverts and brand stories that carry your message.",
     "items": [
         "Corporate and company profile videos", "Promotional and advertising videos",
         "Brand storytelling and campaign videos", "Product and service explainer videos",
         "Interviews and testimonial videos", "Educational and training videos"]},
    {"key": "event", "icon": "spark", "page": "birthday-and-event-videography-addis-ababa",
     "title": "Birthdays, Weddings and Private Events",
     "blurb": "Your celebration, filmed beautifully and delivered to share.",
     "items": [
         "Birthday party videos and highlight films", "Wedding and engagement films",
         "Graduation, baby shower and anniversary coverage", "Family and cultural celebrations",
         "Photo and video packages for private clients", "Short teaser clips for social media"]},
    {"key": "ngo", "icon": "film", "page": "ngo-documentary-production-ethiopia",
     "title": "NGO Documentaries and Campaigns",
     "blurb": "Project stories and awareness campaigns that donors remember.",
     "items": [
         "Project documentation and impact stories", "Awareness and advocacy campaign videos",
         "Donor-facing and reporting videos", "Field interviews and location filming",
         "Formal proposals and quotations", "Frame agreements for repeat work"]},
    {"key": "retainer", "icon": "bolt", "page": "social-media-video-content-ethiopia",
     "title": "Social Media Content Packages",
     "blurb": "Monthly short-form video so your channels never go quiet.",
     "items": [
         "Reels, TikTok and short-form videos", "LinkedIn and Facebook video content",
         "Monthly or quarterly content plans", "Captions, subtitles and cut-downs",
         "Behind-the-scenes and tips content", "Add-ons that keep your audience engaged"]},
    {"key": "photography", "icon": "camera",
     "title": "Professional Photography",
     "blurb": "Images that make your brand look as good as it is.",
     "items": [
         "Corporate and business photography", "Product and commercial photography",
         "Portrait and professional profile photography", "Event and conference photography",
         "Documentary photography", "Brand and marketing photography"]},
    {"key": "studio", "icon": "mic",
     "title": "Studio Production",
     "blurb": "Planned, controlled production in a studio setting.",
     "items": [
         "Studio-based video recording", "Interviews and professional presentations",
         "Educational and training content", "Talk shows and discussion programs",
         "Presenter-led videos", "Product and promotional shoots"]},
    {"key": "documentary", "icon": "layers",
     "title": "Documentary Production",
     "blurb": "Long-form storytelling, from research to delivery.",
     "items": [
         "Corporate and institutional documentaries", "Social impact and development documentaries",
         "Cultural and community documentaries", "Human-interest and personal stories",
         "Research, scripting and location filming", "Editing, subtitles and final delivery"]},
    {"key": "multilingual", "icon": "globe",
     "title": "Multilingual Content",
     "blurb": "Content for audiences in Ethiopia and abroad.",
     "items": [
         "Content in local Ethiopian languages", "Content in foreign languages",
         "Multilingual interviews and presentations", "Language-learning content",
         "Script preparation and localization coordination", "Subtitles and multilingual versions"]},
    {"key": "hosting", "icon": "user",
     "title": "Video Hosting and Presentation",
     "blurb": "Hosts and presenters matched to your language and audience.",
     "items": [
         "Professional video hosts and presenters", "Interview hosts and moderators",
         "Educational video presenters", "Promotional video presenters",
         "Presenter-led business content", "Host coordination and production support"]},
]

TICKER = [
    "Corporate videos", "Birthdays", "Weddings", "Documentaries", "NGO campaigns", "Photography",
    "Social media content", "Graduations", "Brand films", "Multilingual videos", "Studio recording",
]

TRIO = [
    ("Create", "Cinematic video and photography, planned around one clear message."),
    ("Connect", "Content shaped for the people you want to reach, in the languages they speak."),
    ("Convert", "Every video ends with a clear next step, so views turn into enquiries."),
]

AUDIENCES = {
    "business": {
        "eyebrow": "Companies, brands and individuals",
        "title": "Content that grows your brand every month",
        "points": [
            "Company profiles, product films and brand stories",
            "Short-form videos for Instagram, TikTok, Facebook and LinkedIn",
            "Monthly or campaign-based packages, so you always have fresh content",
            "Photography, interviews and testimonial videos",
        ],
        "cta": "Plan my content", "service": "retainer",
    },
    "private": {
        "eyebrow": "Families and private clients",
        "title": "Moments you will want to watch again",
        "points": [
            "Birthdays, weddings, graduations and baby showers",
            "Cultural and family celebrations filmed with care",
            "Highlight film, full coverage and photo gallery options",
            "Clear packages and a quote before you commit",
        ],
        "cta": "Book my event", "service": "event",
    },
    "ngo": {
        "eyebrow": "NGOs and institutions",
        "title": "Documentaries and campaigns donors remember",
        "points": [
            "Project documentation and donor-facing impact stories",
            "Awareness campaigns in local and foreign languages",
            "Formal proposals, quotations and frame agreements for repeat work",
            "Field filming with delivery evidence for your reports",
        ],
        "cta": "Request a proposal", "service": "ngo",
    },
}

# Standardized packages. Scope is described, not priced: every quote follows a short brief.
# When prices are fixed, add a "price" key and show it in merci.html.
PACKAGES = [
    {"key": "business", "label": "Companies & creators", "items": [
        {"name": "Social Content Retainer", "cadence": "Monthly", "service": "retainer",
         "tag": "A steady stream of short videos for your channels.",
         "points": ["Short-form videos for reels, TikTok, Facebook and LinkedIn",
                    "Monthly content plan and filming day",
                    "Captions, subtitles and platform cut-downs",
                    "Review round included each month"],
         "best": "Best for brands that want to post consistently."},
        {"name": "Brand Film", "cadence": "One project", "service": "video", "feature": True,
         "tag": "A signature film that tells who you are.",
         "points": ["Concept, script and storyboard",
                    "Professional filming and sound",
                    "Edit, color, motion graphics and music",
                    "Cut-downs for social media"],
         "best": "Best for launches, company profiles and campaigns."},
        {"name": "Content Partner", "cadence": "Quarterly", "service": "package",
         "tag": "Video, photography and campaign content in one plan.",
         "points": ["Long-form and short-form video every month",
                    "Photography for your website and social media",
                    "Campaign planning across the quarter",
                    "Priority scheduling for new shoots"],
         "best": "Best for growing companies and personal brands."},
    ]},
    {"key": "private", "label": "Private events", "items": [
        {"name": "Celebration Highlights", "cadence": "One event", "service": "event",
         "tag": "Your birthday or party in a film you will keep.",
         "points": ["Video coverage of the key moments",
                    "Edited highlight film with music",
                    "Photo selection from the day",
                    "Short teaser clip for sharing"],
         "best": "Best for birthdays, baby showers and graduations."},
        {"name": "Wedding Story", "cadence": "One event", "service": "event", "feature": True,
         "tag": "The whole day, told like a film.",
         "points": ["Full-day video and photo coverage",
                    "Cinematic highlight film",
                    "Edited photo gallery",
                    "Teaser clip for family and friends"],
         "best": "Best for weddings, engagements and cultural ceremonies."},
        {"name": "Family Memories", "cadence": "Custom", "service": "event",
         "tag": "A keepsake built from your photos and moments.",
         "points": ["Event coverage plus a portrait session",
                    "Keepsake video with music and photos",
                    "Versions for sharing on social media",
                    "Planning call before the day"],
         "best": "Best for anniversaries and family milestones."},
    ]},
    {"key": "ngo", "label": "NGOs & institutions", "items": [
        {"name": "Project Documentary", "cadence": "Project contract", "service": "documentary",
         "tag": "The story of your project, told on film.",
         "points": ["Research, field interviews and location filming",
                    "Scripting, editing and subtitles",
                    "Versions for donors, partners and the public",
                    "Formal proposal and quotation"],
         "best": "Best for project close-outs and donor reporting."},
        {"name": "Awareness Campaign", "cadence": "Campaign", "service": "ngo", "feature": True,
         "tag": "Videos that move people to act.",
         "points": ["Campaign concept and key messages",
                    "Spots, social cut-downs and photography",
                    "Versions in local and foreign languages",
                    "Delivery formats for TV, web and events"],
         "best": "Best for public awareness and advocacy."},
        {"name": "Frame Agreement", "cadence": "Repeat work", "service": "ngo",
         "tag": "One agreed rate for all your video needs.",
         "points": ["Agreed scope and rates across the year",
                    "Impact stories from several project sites",
                    "Faster turnaround with a team that knows you",
                    "Delivery evidence for each assignment"],
         "best": "Best for organizations with ongoing documentation needs."},
    ]},
]

STEPS = [
    ("Brief and consultation", "We learn your goals, audience, message, budget and timeline."),
    ("Concept and scripting", "We develop the concept, creative direction, script and shot plan."),
    ("Production planning", "We arrange crew, equipment, studio, presenters and locations."),
    ("Filming and photography", "We capture professional video and photos in our studio or at your location."),
    ("Edit and post-production", "We handle editing, sound, color, graphics, titles and subtitles."),
    ("Review and delivery", "You give feedback, we revise within the agreed scope and deliver in the right formats."),
]

CLIENTS = [
    "Businesses and private companies", "Government institutions",
    "NGOs and development organizations", "Schools and training providers",
    "Tourism and cultural organizations", "Marketing and communication teams",
    "Entrepreneurs and personal brands",
]

BENEFITS = [
    ("layers", "One team, start to finish", "Concept, filming, editing and delivery handled by one coordinated team."),
    ("camera", "Studio or on location", "Production planned for your space, our studio, or the field."),
    ("globe", "Made for your audience", "Content in Amharic, Afaan Oromoo, Tigrinya, English and more."),
    ("spark", "Story first", "Visual content built around a clear message and a clear next step."),
    ("bolt", "Flexible to your size", "From one birthday film to a full monthly production package."),
    ("building", "Backed by Msigana", "Supported by the wider technology and marketing capabilities of Msigana."),
]

FAQ = [
    ("How much does a video cost?",
     "It depends on the length, number of filming days, locations, crew and the languages you need. Send us a short brief and we reply with a clear quotation. Monthly and quarterly packages are priced per package, so you know your cost in advance."),
    ("Do you film birthdays, weddings and other private events?",
     "Yes. We cover birthdays, weddings, engagements, graduations, baby showers, anniversaries and family or cultural celebrations. You can choose a highlight film, full coverage, photography, or a package that combines them."),
    ("How do I get started?",
     "Use the form on this page, call us or message us on WhatsApp. We arrange a short consultation to understand your goals, then send a quotation and a simple production plan."),
    ("Do you work with NGOs and institutions?",
     "Yes. We produce project documentaries, awareness campaigns and donor-facing impact stories. We prepare formal proposals and quotations, respond to tenders, and set up frame agreements for repeat work."),
    ("Can you produce videos in Amharic, Afaan Oromoo and other languages?",
     "Yes. We produce in local Ethiopian languages and in foreign languages, with scripting, localization coordination, subtitles and multilingual versions depending on your project."),
    ("Do you offer monthly content packages?",
     "Yes. Our retainers cover short-form videos, long-form content and photography on a monthly or quarterly plan, so your channels stay active without a new brief every time."),
    ("How many revisions are included?",
     "We agree the number of review rounds in your quotation. After each round we revise within the agreed scope and deliver the final video in the formats you need."),
    ("Can I talk to you before I decide?",
     "Yes. Every project starts with a free consultation by phone, WhatsApp or in person. We listen to your goals, suggest the right format and send a clear quotation. No commitment."),
    ("Do you partner with agencies, event organizers and schools?",
     "Yes. We work with agencies, event organizers, schools, businesses and other partners, and we offer referral arrangements. Contact us to discuss how we can work together."),
    ("Where do you film?",
     "In our studio in Addis Ababa or on location anywhere in Ethiopia. For larger projects we plan travel and crew as part of the quotation."),
]


# ---------------------------------------------------------------------------
# Landing pages: one focused, indexable page per service people search for.
# ---------------------------------------------------------------------------
LANDING = {
    "corporate-video-production-addis-ababa": {
        "service": "video", "icon": "video", "kicker": "Corporate video",
        "nav": "Corporate videos",
        "meta_title": "Corporate Video Production in Addis Ababa | Company Profile Films | Merci Media",
        "meta": "Professional corporate video production in Addis Ababa: company profiles, brand films, adverts, product and training videos. Free consultation and a clear quote.",
        "h1": "Corporate video production in Addis Ababa",
        "intro": "Your company deserves a film that explains who you are and why people should choose you. Merci Media plans, scripts, films and edits corporate videos that look professional and lead to enquiries.",
        "included": ["Company profile and brand story films", "Promotional and advertising videos",
                     "Product and service explainer videos", "Interviews and customer testimonial videos",
                     "Training and internal communication videos", "Short cut-downs for social media and LinkedIn"],
        "good_for": ["Company launches", "Websites and sales decks", "Tenders and investor pitches", "Recruitment and training"],
        "faq": [("How long does a corporate video take?", "It depends on length and complexity. After a short brief we give you a production plan with dates for filming, first edit and final delivery."),
                ("Can you film at our office?", "Yes. We film on location at your premises or in our studio, and plan lighting and sound for the space."),
                ("Can you make versions for social media?", "Yes. We deliver the main film plus shorter vertical and square versions for Instagram, TikTok, Facebook and LinkedIn.")],
    },
    "birthday-and-event-videography-addis-ababa": {
        "service": "event", "icon": "spark", "kicker": "Birthdays and private events",
        "nav": "Birthdays and events",
        "meta_title": "Birthday & Event Videography in Addis Ababa | Photo and Video | Merci Media",
        "meta": "Birthday, graduation, baby shower, anniversary and family event videography and photography in Addis Ababa. Highlight films and full coverage. Get a quote today.",
        "h1": "Birthday and private event videography in Addis Ababa",
        "intro": "Birthdays, graduations, baby showers, anniversaries and family celebrations pass quickly. We capture the moments that matter and turn them into a film and photos you can share and keep.",
        "included": ["Video coverage of the key moments of your event", "Edited highlight film with music",
                     "Professional photography and edited photo selection", "Short teaser clip for WhatsApp, Instagram and TikTok",
                     "Options for full-event coverage", "A planning call before the day"],
        "good_for": ["Birthday parties", "Graduations", "Baby showers", "Anniversaries and family gatherings"],
        "faq": [("How do I book a date?", "Send us the date, venue and type of event through the form or WhatsApp. We confirm availability and send a quote."),
                ("Do you do photos as well as video?", "Yes. You can book video only, photos only, or a package that combines both."),
                ("How soon do I get the video?", "We agree the delivery date in your quote. Many clients also ask for a short teaser clip to share first.")],
    },
    "wedding-videography-addis-ababa": {
        "service": "event", "icon": "spark", "kicker": "Weddings",
        "nav": "Weddings",
        "meta_title": "Wedding Videography & Photography in Addis Ababa | Merci Media",
        "meta": "Cinematic wedding videography and photography in Addis Ababa. Full-day coverage, highlight film and edited photo gallery for weddings and engagements. Request a quote.",
        "h1": "Wedding videography and photography in Addis Ababa",
        "intro": "Your wedding is a once-in-a-lifetime story. We film and photograph the full day, from preparations to the last dance, and edit it into a cinematic highlight film and a gallery you will treasure.",
        "included": ["Full-day video and photo coverage", "Cinematic highlight film", "Edited photo gallery",
                     "Teaser clip for family and friends", "Cultural and traditional ceremonies covered with care", "Engagement and pre-wedding sessions"],
        "good_for": ["Weddings", "Engagements", "Traditional and cultural ceremonies", "Pre-wedding shoots"],
        "faq": [("Can we meet before the wedding?", "Yes. We hold a planning call or meeting to agree the schedule, key moments and the style you want."),
                ("Do you film traditional ceremonies?", "Yes. We cover cultural and traditional ceremonies and plan the shots with your family."),
                ("What do we receive?", "A highlight film and an edited photo gallery, with options for full ceremony video, delivered in formats that are easy to share.")],
    },
    "ngo-documentary-production-ethiopia": {
        "service": "ngo", "icon": "film", "kicker": "NGO documentaries",
        "nav": "NGO documentaries",
        "meta_title": "NGO Documentary & Campaign Video Production in Ethiopia | Merci Media",
        "meta": "Documentary and campaign video production for NGOs in Ethiopia: project documentation, awareness campaigns and donor impact stories. Proposals, quotations and frame agreements.",
        "h1": "NGO documentary and campaign video production in Ethiopia",
        "intro": "Donors and communities respond to real stories. We produce project documentaries, awareness campaigns and impact videos that show what your work achieves, with field filming across Ethiopia.",
        "included": ["Project documentation and impact stories", "Awareness and advocacy campaign videos",
                     "Donor-facing and reporting videos", "Field interviews and location filming",
                     "Versions in local and foreign languages with subtitles", "Formal proposal and quotation for each project"],
        "good_for": ["Project close-outs", "Donor reporting", "Public awareness campaigns", "Fundraising"],
        "faq": [("Do you respond to tenders?", "Yes. We prepare formal proposals and quotations and respond to relevant tender and procurement opportunities."),
                ("Can we sign a frame agreement?", "Yes. A frame agreement gives you agreed scope and rates for repeat video work across projects."),
                ("Can you film in remote locations?", "Yes. We plan travel, crew and equipment for field filming as part of the quotation.")],
    },
    "social-media-video-content-ethiopia": {
        "service": "retainer", "icon": "bolt", "kicker": "Social media content",
        "nav": "Social media content",
        "meta_title": "Social Media Video Content & Monthly Packages in Ethiopia | Merci Media",
        "meta": "Monthly social media video packages in Ethiopia: reels, TikTok, LinkedIn and Facebook content for businesses and personal brands. Consistent, professional, easy.",
        "h1": "Social media video content for brands in Ethiopia",
        "intro": "Posting consistently is hard. Our monthly and quarterly content packages give you a steady stream of professional short videos, planned around your goals, so your audience keeps seeing you.",
        "included": ["Short-form videos for reels, TikTok, Facebook and LinkedIn", "Monthly content plan and filming day",
                     "Captions, subtitles and platform cut-downs", "Behind-the-scenes and tips content",
                     "Add-on videos when you need more", "Review round included each month"],
        "good_for": ["Businesses and startups", "Personal brands and professionals", "Restaurants, hotels and shops", "Schools and training providers"],
        "faq": [("What is a content retainer?", "A monthly or quarterly package where we plan, film and edit your content on a regular schedule, so you do not need a new brief every time."),
                ("Can we start small?", "Yes. Start with a short package and add more videos as your results grow."),
                ("Do you write the scripts and captions?", "Yes. We plan topics, write short scripts and prepare captions, and you approve before we publish or deliver.")],
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _static_if_exists(path):
    """Return the static URL for `path` if the file exists, otherwise an empty string."""
    try:
        return static(path) if finders.find(path) else ""
    except ValueError:  # manifest storage without collectstatic: fall back to the plain page
        return ""


def _hero():
    """Hero media. Drop files into static/merci/video/ and static/merci/img/ and they are picked up automatically:

        merci/video/hero-desktop.mp4   (or .webm)  - wide showreel, 1080p, under ~8 MB
        merci/video/hero-mobile.mp4    (or .webm)  - vertical 9:16 showreel, 720p, under ~5 MB
        merci/img/hero-desktop.jpg                 - poster for the desktop video
        merci/img/hero-mobile.jpg                  - poster for the phone video
    """
    video_desktop = _static_if_exists("merci/video/hero-desktop.mp4") or _static_if_exists("merci/video/hero-desktop.webm")
    video_mobile = _static_if_exists("merci/video/hero-mobile.mp4") or _static_if_exists("merci/video/hero-mobile.webm")
    return {
        "video_desktop": video_desktop,
        "video_mobile": video_mobile or video_desktop,
        "poster_desktop": _static_if_exists("merci/img/hero-desktop.jpg"),
        "poster_mobile": _static_if_exists("merci/img/hero-mobile.jpg"),
    }


def _json_ld(data):
    # "</" is escaped so the JSON can never close the surrounding <script> tag.
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def _structured_data(site, projects):
    root = site["url"] + "/"
    org_id = root + "#organization"
    same_as = [site[k] for k in ("youtube", "instagram", "tiktok", "linkedin", "facebook", "telegram") if site.get(k)]
    org = {
        "@type": ["ProfessionalService", "LocalBusiness"],
        "@id": org_id,
        "name": BRAND,
        "alternateName": "Merci Media",
        "url": root,
        "logo": site["url"] + static("merci/img/icon-512.png"),
        "image": site["url"] + static("merci/img/og-image.jpg"),
        "description": "Video production, documentaries, photography and social media content for companies, NGOs and individuals in Ethiopia.",
        "slogan": "Create. Connect. Convert.",
        "telephone": site["phone"],
        "email": site["email"],
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": site["address"], "addressLocality": "Addis Ababa", "addressCountry": "ET"},
        "areaServed": [{"@type": "City", "name": "Addis Ababa"}, {"@type": "Country", "name": "Ethiopia"}],
        "parentOrganization": {"@type": "Organization", "name": "Msigana", "url": site["parent_url"]},
        "knowsLanguage": ["am", "om", "ti", "en"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Production services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["title"], "description": s["blurb"]}}
                for s in SERVICES
            ],
        },
    }
    if same_as:
        org["sameAs"] = same_as

    graph = [
        org,
        {"@type": "WebSite", "@id": root + "#website", "url": root, "name": BRAND, "publisher": {"@id": org_id}, "inLanguage": "en"},
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ
            ],
        },
    ]
    for p in projects[:12]:
        graph.append({
            "@type": "VideoObject",
            "name": p.title,
            "description": p.description or f"{p.title}, a {p.get_category_display().lower()} project by {BRAND}.",
            "thumbnailUrl": p.thumbnail_url if p.thumbnail_url.startswith("http") else site["url"] + p.thumbnail_url,
            "uploadDate": p.created_at.date().isoformat(),
            "embedUrl": f"https://www.youtube-nocookie.com/embed/{p.video_id}",
            "publisher": {"@id": org_id},
        })
    return _json_ld({"@context": "https://schema.org", "@graph": graph})


def _landing_structured_data(site, slug, page, url):
    root = site["url"] + "/"
    graph = [
        {
            "@type": "Service",
            "name": page["h1"],
            "description": page["meta"],
            "serviceType": page["nav"],
            "url": url,
            "provider": {"@id": root + "#organization"},
            "areaServed": [{"@type": "City", "name": "Addis Ababa"}, {"@type": "Country", "name": "Ethiopia"}],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": root},
                {"@type": "ListItem", "position": 2, "name": page["nav"], "item": url},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faq"]
            ],
        },
    ]
    return _json_ld({"@context": "https://schema.org", "@graph": graph})


def _services_structured_data(site, url):
    root = site["url"] + "/"
    graph = [
        {
            "@type": "ItemList",
            "name": "Merci Media services",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "item": {
                    "@type": "Service", "name": svc["title"], "description": svc["blurb"],
                    "provider": {"@id": root + "#organization"},
                    "areaServed": {"@type": "Country", "name": "Ethiopia"},
                    "url": f"{url}#{svc['key']}",
                }}
                for i, svc in enumerate(SERVICES, 1)
            ],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": root},
                {"@type": "ListItem", "position": 2, "name": "Services", "item": url},
            ],
        },
    ]
    return _json_ld({"@context": "https://schema.org", "@graph": graph})


def _notify(inquiry):
    """Email the team. The inquiry is already saved, so a mail failure never reaches the visitor."""
    try:
        recipient = getattr(settings, "MERCI_INQUIRY_EMAIL", None) or settings.DEFAULT_FROM_EMAIL
        body = (
            f"Name: {inquiry.full_name}\nPhone: {inquiry.phone}\nEmail: {inquiry.email or '-'}\n"
            f"Organization: {inquiry.organization or '-'}\nService: {inquiry.get_service_display()}\n"
            f"Language: {inquiry.get_language_display() or '-'}\nTimeline: {inquiry.get_timeline_display() or '-'}\n"
            f"Budget: {inquiry.budget or '-'}\n\n{inquiry.project_description}"
        )
        EmailMessage(
            subject=f"New Merci inquiry: {inquiry.get_service_display()} from {inquiry.full_name}",
            body=body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            to=[recipient],
            reply_to=[inquiry.email] if inquiry.email else None,
        ).send(fail_silently=False)
    except Exception:
        logger.exception("Could not send Merci inquiry email")


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------
def _process_form(request):
    """Handle the quote form for any page. Returns (form, redirect_response_or_None)."""
    if request.method == "POST":
        form = MerciInquiryForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data.get("website"):  # a filled honeypot is a bot: pretend it worked
                _notify(form.save())
            return form, redirect(f"{request.path}?sent=1#inquiry")
        return form, None
    service = request.GET.get("service", "")
    valid = {key for key, _ in MerciInquiry.SERVICE_CHOICES}
    return MerciInquiryForm(initial={"service": service if service in valid else ""}), None


def shared_context(request):
    """Values every Merci page needs (header, footer, contact buttons). Also used by the blog app."""
    return {
        "brand": BRAND,
        "site": get_site(),
        "landing_links": [(slug, p["nav"]) for slug, p in LANDING.items()],
        # Pages without a quote form send the visitor to the form on the home page.
        "quote_href": reverse("merci:home") + "#inquiry",
    }


def _base_context(request, form, site, path="/"):
    context = shared_context(request)
    context.update({
        "site": site,
        "form": form,
        "form_action": request.path,
        "quote_href": "#inquiry",  # this page has its own form
        "sent": request.GET.get("sent") == "1",
        "more_open": form.optional_has_errors if request.method == "POST" else False,
    })
    return context


def merci_home(request):
    form, done = _process_form(request)
    if done:
        return done

    site = get_site()
    projects = list(MerciProject.objects.filter(is_published=True))
    photos = list(MerciPhoto.objects.filter(is_published=True))
    used_categories = {p.category for p in projects}
    used_photo_categories = {p.category for p in photos}

    context = _base_context(request, form, site)
    context.update({
        "canonical": site["url"] + "/",
        "hero": _hero(),
        "structured_data": _structured_data(site, projects),
        "services": SERVICES,
        "ticker": TICKER,
        "trio": TRIO,
        "audiences": AUDIENCES,
        "package_groups": PACKAGES,
        "steps": STEPS,
        "clients": CLIENTS,
        "benefits": BENEFITS,
        "faq": FAQ,
        "projects": projects,
        "featured": projects[0] if projects else None,
        "work_categories": [(k, v) for k, v in MerciProject.CATEGORY_CHOICES if k in used_categories],
        "photos": photos,
        "photo_categories": [(k, v) for k, v in MerciPhoto.CATEGORY_CHOICES if k in used_photo_categories],
        "testimonials": MerciTestimonial.objects.filter(is_published=True),
        "youtube_channel_url": site["youtube"],
    })
    return render(request, "merci/merci.html", context)


def landing(request, slug):
    page = LANDING.get(slug)
    if page is None:
        raise Http404("No such page")
    form, done = _process_form(request)
    if done:
        return done

    site = get_site()
    url = f"{site['url']}/{slug}/"
    context = _base_context(request, form, site)
    context.update({
        "canonical": url,
        "page": page,
        "slug": slug,
        "steps": STEPS,
        "related": [(s, p["nav"]) for s, p in LANDING.items() if s != slug],
        "testimonials": MerciTestimonial.objects.filter(is_published=True)[:3],
        "structured_data": _landing_structured_data(site, slug, page, url),
    })
    return render(request, "merci/landing.html", context)


def services_page(request):
    form, done = _process_form(request)
    if done:
        return done
    site = get_site()
    url = site["url"] + "/services/"
    context = _base_context(request, form, site)
    context.update({
        "canonical": url,
        "services": SERVICES,
        "package_groups": PACKAGES,
        "steps": STEPS,
        "faq": FAQ[:5],
        "structured_data": _services_structured_data(site, url),
    })
    return render(request, "merci/services.html", context)


@require_GET
def robots_txt(request):
    site = get_site()
    lines = ["User-agent: *", "Allow: /", "Disallow: /admin/", "", f"Sitemap: {site['url']}/sitemap.xml"]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


@require_GET
def sitemap_xml(request):
    site = get_site()
    today = timezone.now().date().isoformat()
    rows = [(f"{site['url']}/", today, "1.0", "weekly"),
            (f"{site['url']}/services/", today, "0.9", "monthly"),
            (f"{site['url']}/blog/", today, "0.8", "weekly")]
    rows += [(f"{site['url']}/{slug}/", today, "0.9", "monthly") for slug in LANDING]
    try:
        from blog.models import Post
        rows += [(f"{site['url']}/blog/{p.slug}/", p.updated_at.date().isoformat(), "0.7", "monthly") for p in Post.objects.all()]
    except Exception:  # blog tables not migrated yet: the rest of the sitemap still works
        logger.exception("Could not add blog posts to the sitemap")
    body = "".join(
        f"  <url><loc>{loc}</loc><lastmod>{mod}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>\n"
        for loc, mod, prio, freq in rows
    )
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n"
    return HttpResponse(xml, content_type="application/xml")
