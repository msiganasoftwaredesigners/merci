# Merci Media & Digitals: whole site

The entire project now serves the Merci site. Msigana's old public pages are no longer routed
(their routes are archived in msigana_ecommerce/legacy_msigana_urls.py).

## URLs
    /                                                   home
    /corporate-video-production-addis-ababa/            landing page
    /birthday-and-event-videography-addis-ababa/        landing page
    /wedding-videography-addis-ababa/                   landing page
    /ngo-documentary-production-ethiopia/               landing page
    /social-media-video-content-ethiopia/               landing page
    /services/                                          all services (jump menu, packages, process, FAQ, quote form)
    /blog/   /blog/<slug>/                              blog (search, topics, pagination, related posts, share, quote CTA)
    /news/ and /news/<slug>/                            301 redirects to /blog/ (old Msigana addresses)
    /sitemap.xml  /robots.txt  /admin/
    /merci/                                             301 redirect to /

## Install
    python manage.py migrate                    # migrations 0004 and 0005
    python manage.py makemigrations --check     # expect: No changes detected
    python manage.py test merci
    python manage.py collectstatic              # production only

## Before launch
1. .env ALLOWED_HOSTS_PROD must include: mercimedia.et,www.mercimedia.et
2. Point DNS and SSL for mercimedia.et at the server.
3. Optional settings:
       MERCI_SITE = {"phone": "+251...", "phone_display": "+251 .. ... ....", "whatsapp": "251...",
                     "email": "hello@mercimedia.et", "telegram": "", "youtube": "", "instagram": "",
                     "tiktok": "", "linkedin": "", "facebook": "", "ga_id": "G-XXXXXXXXXX"}
       MERCI_INQUIRY_EMAIL = "hello@mercimedia.et"
4. Search Console: add mercimedia.et and submit https://mercimedia.et/sitemap.xml
5. Create a Google Business Profile for Merci Media (Addis Ababa). This is the biggest local-search factor.

## Add your media
Hero showreel (picked up automatically if the files exist):
    static/merci/video/hero-desktop.mp4  (16:9, 1080p, under ~8 MB)
    static/merci/video/hero-mobile.mp4   (9:16, 720p, under ~5 MB)
    static/merci/img/hero-desktop.jpg    static/merci/img/hero-mobile.jpg  (posters)
In /admin/: Merci projects (YouTube links, optional Shorts link for phones), photos, testimonials.

## Edit wording
Services, packages, FAQ, process and the 5 landing pages are plain data at the top of merci/views.py.

## Blog
Uses the existing blog app and data (no new migration). Write articles in /admin/ under Blog > Posts:
title, cover image (required), content (rich editor), and optionally a Category. The slug and the short
description (used as the meta description) are filled in automatically. New posts appear on /blog/ and in
/sitemap.xml straight away. Search results and topic filters are marked noindex; the main list is indexed.
Tip: publish 2 to 4 short articles a month on topics people search for ("birthday video ideas in Addis Ababa",
"wedding videographer checklist", "how much does a company video cost").
