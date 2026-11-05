from .base import *
from decouple import  config


DEBUG = True

SECRET_KEY = config('SECRET_KEY')


# ALLOWED_HOSTS = config('ALLOWED_HOSTS_DEV').split(',')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mercimedia.et', 'www.mercimedia.et']


# Appication definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'heads.apps.HeadsConfig',
    'blog.apps.BlogConfig', 
    'advertizement',
    'footer.apps.FooterConfig',
    'contact.apps.ContactConfig',
    'customers.apps.CustomersConfig',
    'nested_admin',
    'rest_framework',
    'merci.apps.MerciConfig',
    'tailwind',
    'theme',
    'django_quill',
    'merci_service',
    'django_browser_reload',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django_recaptcha',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DEV_DATABASE_NAME'),
        'USER': config('DEV_DATABASE_USER'),
        'PASSWORD': config('DEV_DATABASE_PASSWORD'),
        'HOST': config('DEV_DATABASE_HOST'),
        'PORT': config('DEV_DATABASE_PORT'),
    }
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'merci.middleware.MerciHostMiddleware',  # serves mercimedia.et from merci.host_urls
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TAILWIND_APP_NAME = 'theme'


