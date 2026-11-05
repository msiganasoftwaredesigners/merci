from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path("payment/", views.direct_payment_page, name='direct_payment_page'),
    path('payment/<int:registration_id>/', views.payment, name='payment'),
    path('bank_payment/<int:registration_id>/', views.bank_payment, name='bank_payment'),
    path('success/', views.success, name='success'),
]
