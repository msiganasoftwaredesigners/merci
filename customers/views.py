from django.shortcuts import render, redirect
from .forms import RegistrationForm, PaywithbankForm, DirectPaymentForm
from .models import Registration

def register(request):
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            registration = reg_form.save()
            return redirect('payment', registration_id=registration.id)
    else:
        reg_form = RegistrationForm()
    return render(request, 'register.html', {'form': reg_form})


def direct_payment_page(request):
    if request.method == 'POST':
        reg_form = DirectPaymentForm(request.POST)
        if reg_form.is_valid():
            registration = reg_form.save()
            return redirect('payment', registration_id=registration.id)
    else:
        reg_form = DirectPaymentForm()
    return render(request, 'direct_payment_page.html', {'form': reg_form})


def payment(request, registration_id):
    registration = Registration.objects.get(id=registration_id)
    class_type = registration.class_type
    duration = registration.duration

    pricing = {
        'O2O': {1: 600, 2: 1100, 3: 1500},
        'SG': {1: 1000, 2: 1700, 3: 2200},
        'PR': {1: 2000, 2: 3500, 3: 4500},
    }

    total_amount = pricing.get(class_type, {}).get(duration, 0)
    request.session['total_amount'] = total_amount  # Store in session

    if request.method == 'POST':
        if 'pay_with_bank' in request.POST:
            return redirect('bank_payment', registration_id=registration.id)
        # Handle other payment options here (e.g., Chapa)
    
    return render(request, 'payment.html', {'registration': registration, 'total_amount': total_amount})


from django.shortcuts import render, redirect
from .forms import RegistrationForm, PaywithbankForm
from .models import Registration, BankDetail

from django.shortcuts import render, redirect
from .forms import PaywithbankForm
from .models import Registration, BankDetail

def bank_payment(request, registration_id):
    registration = Registration.objects.get(id=registration_id)
    bank_details = BankDetail.objects.all()
    total_amount = request.session.get('total_amount', 0)  # Retrieve from session

    if request.method == 'POST':
        bank_form = PaywithbankForm(request.POST, request.FILES)
        if bank_form.is_valid():
            bank_payment = bank_form.save(commit=False)
            bank_payment.total_amount = total_amount  # Set total amount here
            bank_payment.save()
            registration.bank_payment = bank_payment
            registration.save()
            return redirect('success')
    else:
        bank_form = PaywithbankForm()

    context = {
        'bank_form': bank_form,
        'registration': registration,
        'bank_details': bank_details,
        'total_amount': total_amount,
    }
    return render(request, 'bank_payment.html', context)


def success(request):
    return render(request, 'success.html')
