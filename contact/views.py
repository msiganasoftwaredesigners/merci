from .models import ContactMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import FormWithCaptcha

import requests
from django.conf import settings

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('your_name')
        number = request.POST.get('your_number')
        email = request.POST.get('your_email')
        message = request.POST.get('message')
        captcha_response = request.POST.get('g-recaptcha-response')  # Get the reCAPTCHA response

        # Verify the reCAPTCHA response
        captcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        captcha_data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,  # Your reCAPTCHA secret key
            'response': captcha_response,
        }
        captcha_verify = requests.post(captcha_url, data=captcha_data)
        captcha_result = captcha_verify.json()

        if not captcha_result.get('success'):  # If reCAPTCHA is not valid
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('contact-us')

        # If reCAPTCHA is valid, process the form
        contact_message = ContactMessage(
            name=name,
            number=number,
            email=email,
            message=message
        )
        contact_message.save()

        # Send an email notification to admin
        subject = f'New Contact Message from {name}'
        email_message = f"Name: {name}\nNumber: {number}\nEmail: {email}\nMessage: {message}"
        send_mail(
            subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        # Send a confirmation email to the user
        user_subject = 'Thank You for Contacting Us'
        user_message = (
            f"Hello {name},\n\n"
            "Thank you for reaching out to us. We have received your message and will get back to you within 24 hours.\n\n"
            "Best regards,\n"
            "The Msigana Team"
        )
        send_mail(
            user_subject,
            user_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],  # Sending confirmation email to the user's email
            fail_silently=False,
        )

        # Display a success message to the user
        messages.success(request, 'Your message has been sent successfully! We will get back to you soon!')
        return redirect('contact-us')

    context = {
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY, 
        "captcha": FormWithCaptcha
    }
    return render(request, 'contact-us.html', context)
