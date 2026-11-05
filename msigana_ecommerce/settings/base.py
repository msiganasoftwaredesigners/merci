import os
from pathlib import Path
from decouple import  config


BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = config('DEBUG', default=False, cast=bool)


ACCOUNT_EMAIL_VERIFICATION = 'none'  
LOGIN_REDIRECT_URL = '/'  
SOCIALACCOUNT_QUERY_EMAIL = True  


TAILWIND_APP_NAME = 'theme'


ROOT_URLCONF = 'msigana_ecommerce.urls'


INTERNAL_IPS = [
    "127.0.0.1",
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'footer.context_processors.footer',
                'heads.context_processors.head_contents',
                'advertizement.context_processors.favicon',

            ],
        },
    },
]

WSGI_APPLICATION = 'msigana_ecommerce.wsgi.application'


    

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
    
]


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [ 
    BASE_DIR / '../static'
    ]
STATIC_ROOT = BASE_DIR / '../staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / '../mediafiles'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.CustomUser'


# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': config('GOOGLE_CLIENT_ID'),
#             'secret': config('GOOGLE_SECRET'),
#         }
#     },
#     'facebook': {
#         'APP': {

#             'client_id': config('FACEBOOK_CLIENT_ID'),
#             'secret': config('FACEBOOK_SECRET'),
#         },
#          'SCOPE': ['email', 'public_profile', 'user_friends'],
#     }
# }


CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERY_WORKER_CONCURRENCY = 4
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

ACCOUNT_FORMS = {'signup': 'users.forms.CustomSignupForm'}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'


SOCIALACCOUNT_ADAPTER = 'users.adapters.account_adapter.CustomSocialAccountAdapter'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
ADMIN_EMAIL = config('ADMIN_EMAIL')

RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = config('RECAPTCHA_REQUIRED_SCORE', cast=float)





EMAIL_TIMEOUT = 10