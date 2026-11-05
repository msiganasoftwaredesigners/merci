from django.shortcuts import render
from users.forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from blog.models import Post, Category, Business_line
from django.shortcuts import get_object_or_404, render

import os


def home(request):
    categories = Category.objects.all()
    posts_with_category = Post.objects.filter(category__name='home').order_by('-updated_at', '-created_at')
    business_lines = Business_line.objects.all().order_by("updated_at", "created_at")
    return render(request, 'index.html', {'posts': posts_with_category, 'categories': categories, 'business_lines': business_lines})

def business_line_detail(request, slug):

    business_line = get_object_or_404(
        Business_line,
        slug=slug
    )

    business_line.views_count += 1
    business_line.save()

    return render(
        request,
        "business_line_detail.html",
        {
            "business_line": business_line,
            "gallery": business_line.gallery.all(),
            "services": business_line.services.all(),
        }
    )

def services(request):
    categories = Category.objects.all()
    posts_with_category = Post.objects.filter(category__name='home')
    return render(request, 'services.html', {'posts': posts_with_category, 'categories': categories})

def about_us(request):
    offers = ["Live Class", "Self-Paced", "Premium", "B2B"]
    return render(request, 'about-us.html', {'offers': offers})

def privacy_policy(request):
    return render(request, 'privacy-policy.html')
def service_detail(request, slug):
    business_line = Business_line.objects.get(slug=slug)
    return render(request, 'service_detail.html', {'business_line': business_line})




@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return JsonResponse({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'address': user.address,
            })
    else:
        form = ProfileForm(instance=request.user)
    orders = request.user.order_set.order_by('-order_date')[:6]
    liked_products = request.user.liked_products.all()

    return render(request, 'profile.html', {'form': form, 'orders': orders, 'liked_products': liked_products})

# def ads_txt(request):
#     # Path to the Ads.txt file
#     ads_txt_path = os.path.join(settings.BASE_DIR, '../static', 'ads.txt')

#     # Read the contents of the Ads.txt file
#     with open(ads_txt_path, 'r') as f:
#         ads_txt_content = f.read()

#     # Return the contents of the Ads.txt file as the HTTP response
#     return HttpResponse(ads_txt_content, content_type='text/plain')