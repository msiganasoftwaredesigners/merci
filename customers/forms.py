from .models import Paywithbank, BankDetail
from .models import Paywithbank
from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'full_name', 'phone_number', 'address', 'age', 'education_level', 'education_other',
            'occupation', 'mother_tongue', 'mother_tongue_other', 'proficiency_level', 'class_type', 'class_type_other', 'duration'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'phone_number': forms.TextInput(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'address': forms.TextInput(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'age': forms.NumberInput(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'education_level': forms.Select(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'education_other': forms.TextInput(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm', 'style': 'display:none;'}),
            'occupation': forms.TextInput(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'mother_tongue': forms.Select(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'mother_tongue_other': forms.TextInput(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm', 'style': 'display:none;'}),
            'proficiency_level': forms.Select(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'class_type': forms.Select(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'class_type_other': forms.TextInput(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm', 'style': 'display:none;'}),
            'duration': forms.Select(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
        }


class DirectPaymentForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'full_name', 'phone_number', 'class_type', 'class_type_other', 'duration'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'phone_number': forms.TextInput(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'class_type': forms.Select(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
            'class_type_other': forms.TextInput(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm', 'style': 'display:none;'}),
            'duration': forms.Select(attrs={'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm'}),
        }


class PaywithbankForm(forms.ModelForm):
    class Meta:
        model = Paywithbank
        fields = ['screenshot', 'bank_detail', 'ref_number', 'user_bank_account_name']
        widgets = {
            'screenshot': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none'
            }),
            'bank_detail': forms.Select(attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500'
            }),
            'ref_number': forms.TextInput(attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500'
            }),
            'user_bank_account_name': forms.TextInput(attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500'
            }),
        }
