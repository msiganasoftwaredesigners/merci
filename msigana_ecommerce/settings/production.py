from .base import *
from decouple import  config

DEBUG = False


SECRET_KEY = config('SECRET_KEY')


ALLOWED_HOSTS = config('ALLOWED_HOSTS_PROD').split(',')




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'users.apps.UsersConfig',
    'footer.apps.FooterConfig',
    'contact.apps.ContactConfig',
    'blog.apps.BlogConfig', 
    'heads.apps.HeadsConfig',
    'advertizement.apps.AdvertizementConfig',
    'customers.apps.CustomersConfig',
    'nested_admin',
    'rest_framework',
    'merci.apps.MerciConfig',
    'merci_service',
    'tailwind',
    'theme',
    'django_quill',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django_recaptcha',
    
]


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('PROD_DATABASE_NAME'),
#         'USER': config('PROD_DATABASE_USER'),
#         'PASSWORD': config('PROD_DATABASE_PASSWORD'),
#         'HOST': config('PROD_DATABASE_HOST'),
#         'PORT': config('PROD_DATABASE_PORT'),
#         # 'OPTIONS': {
#         #     'sslmode': 'require',
#         # },
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'msigana_new_db',
        'USER': 'msigana_admin',  # Changed to match POSTGRES_USER
        'PASSWORD': 'Msiganadotcom11@#',
        'HOST': 'db',  
        'PORT': '5432', 
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'merci.middleware.MerciHostMiddleware',  # serves mercimedia.et from merci.host_urls
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True



# # HTTPS settings
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# SECURE_SSL_REDIRECT = False



# HSTS settings
# SECURE_HSTS_SECONDS = 31536000 # 1 year
# SECURE_HSTS_PRELOAD = False
# SECURE_HSTS_INCLUDE_SUBDOMAINS =   False


# 
SECURE_BROWSER_XSS_FILTER = True


CSRF_COOKIE_HTTPONLY = True



SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")



CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
