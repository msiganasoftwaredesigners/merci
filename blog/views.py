import html
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, render
from django.utils.html import strip_tags

from merci.views import _json_ld, shared_context

from .models import Category, Post

POSTS_PER_PAGE = 9


def _absolute(site, url):
    return url if url.startswith("http") else site["url"] + url


def post_list(request):
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()

    posts = Post.objects.select_related("category").order_by("-created_at")
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(short_description__icontains=query))
    category = None
    if category_slug:
        category = Category.objects.filter(slug=category_slug).first()
        posts = posts.filter(category__slug=category_slug)

    page = Paginator(posts, POSTS_PER_PAGE).get_page(request.GET.get("page"))
    items = list(page.object_list)
    filtered = bool(query or category_slug)
    # The newest article is shown large on the first, unfiltered page.
    featured = items[0] if items and page.number == 1 and not filtered else None
    rest = items[1:] if featured else items

    context = shared_context(request)
    site = context["site"]
    canonical = site["url"] + "/blog/" + (f"?page={page.number}" if page.number > 1 and not filtered else "")
    keep = {k: v for k, v in (("q", query), ("category", category_slug)) if v}
    context.update({
        "canonical": canonical,
        "noindex": filtered,  # search and filter results are not indexed, only the main list
        "page": page,
        "featured": featured,
        "posts": rest,
        "query": query,
        "category": category,
        "categories": Category.objects.filter(posts__isnull=False).distinct().order_by("name"),
        "pager_qs": urlencode(keep) + ("&" if keep else ""),
        "structured_data": _json_ld({
            "@context": "https://schema.org",
            "@type": "Blog",
            "name": "Merci Media Blog",
            "url": site["url"] + "/blog/",
            "description": "Video production tips, event ideas and stories from Merci Media in Addis Ababa.",
            "publisher": {"@id": site["url"] + "/#organization"},
        }),
    })
    return render(request, "blog/list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("category"), slug=slug)
    Post.objects.filter(pk=post.pk).update(views_count=F("views_count") + 1)
    post.refresh_from_db()

    related = Post.objects.exclude(pk=post.pk)
    if post.category_id:
        related = related.filter(category=post.category)
    related = list(related.order_by("-created_at")[:3])
    if len(related) < 3:  # top up with the newest other articles
        extra = Post.objects.exclude(pk__in=[post.pk] + [r.pk for r in related]).order_by("-created_at")
        related += list(extra[: 3 - len(related)])

    body = str(post.content.html) if post.content else ""
    words = len(html.unescape(strip_tags(body)).split())

    context = shared_context(request)
    site = context["site"]
    url = f"{site['url']}/blog/{post.slug}/"
    image = _absolute(site, post.image.url) if post.image else ""
    context.update({
        "canonical": url,
        "post": post,
        "body": body,
        "reading_minutes": max(1, round(words / 200)),
        "related": related,
        "share_url": url,
        "og_image": image,
        "structured_data": _json_ld({
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "BlogPosting",
                    "headline": post.get_plain_title()[:110],
                    "description": post.short_description,
                    "image": [image] if image else [],
                    "datePublished": post.created_at.isoformat(),
                    "dateModified": post.updated_at.isoformat(),
                    "mainEntityOfPage": url,
                    "author": {"@type": "Organization", "name": context["brand"], "url": site["url"] + "/"},
                    "publisher": {"@id": site["url"] + "/#organization"},
                    "articleSection": post.category.name if post.category_id else "Blog",
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": site["url"] + "/"},
                        {"@type": "ListItem", "position": 2, "name": "Blog", "item": site["url"] + "/blog/"},
                        {"@type": "ListItem", "position": 3, "name": post.get_plain_title(), "item": url},
                    ],
                },
            ],
        }),
    })
    return render(request, "blog/detail.html", context)
