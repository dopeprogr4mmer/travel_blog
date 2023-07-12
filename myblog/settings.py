import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=os.environ.get('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['travelrealindia.in', '34.125.25.208', '127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
	#'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myposts',
    'newsletter',
    'gallery',
    'contactus',
    'profiles.apps.ProfilesConfig',
    'tinymce',
    'crispy_forms',
    'filebrowser',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'imagekit'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]


WSGI_APPLICATION = 'myblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
 
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

#tinymce
TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'theme': 'modern',  
    'contextmenu': 'formats | link image',
    'menubar': False,
    'inline': False,
    'statusbar': True,
    'width': 'auto',
    'remove_script_host' : False,
    'convert_urls' : False,
    #'height': 360,
    #'width':1120,
    'clean_on_startup':True,
    'custom_undo_redo_levels': 20,
    'plugins': '''textcolor save link image media preview codesample contextmenu
            table code lists fullscreen insertdatetime nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists charmap print 
            link image preview codesample contextmenu table code lists hr
            anchor pagebreak''',
    'toolbar1': 
                '''fullscreen | formatselect | bold italic underline | fontselect  fontsizeselect |
                forecolor backcolor | alignleft aligncenter alignright alignjustify |
                bullist numlist | outdent indent | table | link image | codesample | preview code''',
    'toolbar2': 'visualblocks visualchars | charmap hr pagebreak nonbreaking anchor | code',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True         
}

MAILCHIMP_API_KEY = ''
MAILCHIMP_DATA_CENTER =''
MAILCHIMP_EMAIL_LIST_ID = ''

FILEBROWSER_DIRECTORY = 'uploads/'
DIRECTORY = 'uploads/'
#FILEBROWSER_DIRECTORY = getattr(settings, "FILEBROWSER_DIRECTORY", 'uploads/')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

#auth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

LOGIN_REDIRECT_URL = 'myposts:index'