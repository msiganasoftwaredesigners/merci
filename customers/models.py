from django.db import models
import time
import random
import string
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import uuid

class BankDetail(models.Model):
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.bank_name} - {self.account_name} - {self.account_number}"

class Paywithbank(models.Model):
    total_amount = models.DecimalField(max_digits=11, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_no = models.CharField(max_length=100, blank=False)
    payment_status = models.BooleanField(default=True)
    screenshot = models.ImageField(upload_to='images/bank', blank=False)
    bank_detail = models.ForeignKey(BankDetail, on_delete=models.CASCADE)
    ref_number = models.CharField(max_length=200, unique=True)
    user_bank_account_name = models.CharField(max_length=200)
    paid_by_bank = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.transaction_no:
            self.transaction_no = str(int(time.time() * 1000)) + ''.join(random.choices(string.ascii_letters + string.digits, k=3))

        try:
            this = Paywithbank.objects.get(id=self.id)
            if this.screenshot != self.screenshot:
                this.screenshot.delete(save=False)
        except Paywithbank.DoesNotExist:
            pass

        if self.screenshot:
            img = Image.open(self.screenshot)
            output = BytesIO()
            img_format = img.format
            img.save(output, format=img_format, quality=75)
            output.seek(0)
            upload_path = 'images/bank/{}.{}'.format(uuid.uuid4(), img_format.lower())
            self.screenshot = ContentFile(output.read(), upload_path)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.screenshot.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.transaction_no


class Registration(models.Model):
    HIGH_SCHOOL = 'HS'
    COLLEGE = 'CL'
    DEGREE = 'DG'
    OTHER_EDUCATION = 'OT'
    EDUCATION_LEVEL_CHOICES = [
        (HIGH_SCHOOL, 'High School'),
        (COLLEGE, 'College'),
        (DEGREE, 'Degree'),
        (OTHER_EDUCATION, 'Other'),
    ]
    
    AMHARIC = 'AM'
    TIGRINYA = 'TG'
    OTHER_LANGUAGE = 'OT'
    MOTHER_TONGUE_CHOICES = [
        (AMHARIC, 'Amharic'),
        (TIGRINYA, 'Tigrinya'),
        (OTHER_LANGUAGE, 'Other'),
    ]
    
    NO_EXPERIENCE = 'NE'
    BEGINNER = 'BE'
    INTERMEDIATE = 'IN'
    ADVANCED = 'AD'
    PROFICIENCY_LEVEL_CHOICES = [
        (NO_EXPERIENCE, 'No Experience'),
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]
    
    ONE_TO_ONE = 'O2O'
    SMALL_GROUP = 'SG'
    PREMIUM = 'PR'
    OTHER_CLASS = 'OT'
    CLASS_TYPE_CHOICES = [
        (ONE_TO_ONE, 'One to One'),
        (SMALL_GROUP, 'Small Group'),
        (PREMIUM, 'Premium'),
        (OTHER_CLASS, 'Other'),
    ]
    
    DURATION_CHOICES = [
        (1, 'One Month'),
        (2, 'Two Months'),
        (3, 'Three Months'),
    ]
    
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    education_level = models.CharField(max_length=2, choices=EDUCATION_LEVEL_CHOICES, blank=True, null=True)
    education_other = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_tongue = models.CharField(max_length=2, choices=MOTHER_TONGUE_CHOICES, blank=True, null=True)
    mother_tongue_other = models.CharField(max_length=100, blank=True, null=True)
    proficiency_level = models.CharField(max_length=2, choices=PROFICIENCY_LEVEL_CHOICES, blank=True, null=True)
    class_type = models.CharField(max_length=3, choices=CLASS_TYPE_CHOICES)
    class_type_other = models.CharField(max_length=100, blank=True, null=True)
    duration = models.IntegerField(choices=DURATION_CHOICES, default=1)

    bank_payment = models.OneToOneField('Paywithbank', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name
