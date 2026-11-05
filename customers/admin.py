# from .models import BankDetail
# from django.contrib import admin
# from msigana_ecommerce.admin_site import admin_site
# from .models import Registration, Paywithbank

# # Registration Admin
# class RegistrationAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'phone_number', 'education_level', 'class_type', 'bank_payment')
#     list_filter = ('education_level', 'class_type', 'mother_tongue')
#     search_fields = ('full_name', 'phone_number', 'occupation')
#     readonly_fields = ('bank_payment',)
#     ordering = ('-id',)

#     def has_delete_permission(self, request, obj=None):
#         return True
# from django.contrib import admin
# from .models import BankDetail, Paywithbank


# class BankDetailAdmin(admin.ModelAdmin):
#     list_display = ('bank_name', 'account_name', 'account_number')
#     search_fields = ('bank_name', 'account_name')


# class PaywithbankAdmin(admin.ModelAdmin):
#     list_display = ('transaction_no', 'get_bank_name', 'total_amount', 'payment_status', 'payment_date')
#     search_fields = ('transaction_no', 'user_bank_account_name', 'ref_number')
#     list_filter = ('payment_status', 'payment_date', 'bank_detail__bank_name')
#     readonly_fields = ('transaction_no','payment_date','total_amount', 'payment_status','bank_detail', 'screenshot')

#     def get_bank_name(self, obj):
#         return obj.bank_detail.bank_name
#     get_bank_name.short_description = 'Bank Name'

# # If you have other models to register
# # from .models import OtherModel
# # admin.site.register(OtherModel)


# # Registering the models with the admin site
# admin_site.register(Registration, RegistrationAdmin)
# admin_site.register(Paywithbank, PaywithbankAdmin)
# admin_site.register(BankDetail, BankDetailAdmin)


