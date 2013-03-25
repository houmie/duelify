# Django settings for duelify project.

LOGIN_URL = '/login/'

AUTH_USER_MODEL = 'duelify_app.User'

SITE_HOST = '127.0.0.1:8000'
DEFAULT_FROM_EMAIL = 'houmie@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'houmie@gmail.com'
EMAIL_HOST_PASSWORD = 'M1thra2503GM'
EMAIL_USE_TLS = True
SERVER_EMAIL = 'houmie@gmail.com'
EMAIL_SUBJECT_PREFIX = '[duelify]'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Hooman', 'hooman@venuscloud.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'duelifydb',                      # Or path to database file if using sqlite3.
        'USER': 'django_user',                      # Not used with sqlite3.
        'PASSWORD': 'houmie123',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

PIPELINE_YUGLIFY_BINARY = '/home/hooman/venuscloud/duelify-env/node_modules/yuglify/bin/yuglify'
PIPELINE_CLOSURE_BINARY = '/home/hooman/venuscloud/duelify-env/bin/closure'
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
#PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.closure.ClosureCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'

PIPELINE_CSS = {
    'duelify_css': {
        'source_filenames': (
          'duelify/duelify.css',          
        ),
        'output_filename': 'duelify/duelify.min.css',        
    },
    'bootstrap_datepicker_css': {
        'source_filenames': (
          'bootstrap-datepicker/css/datepicker.css',          
        ),
        'output_filename': 'bootstrap-datepicker/css/datepicker.min.css',        
    },    
}

PIPELINE_JS = {
    'duelify_js': {
        'source_filenames': (
          'duelify/duelify.js',          
        ),
        'output_filename': 'duelify/duelify.min.js',
    },
   'bootstrap_datepicker_js': {
        'source_filenames': (
          'bootstrap-datepicker/js/bootstrap-datepicker.js',
        ),
        'output_filename': 'bootstrap-datepicker/js/bootstrap-datepicker.min.js',
    },   
}


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['duelify.com', 'www.duelify.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/hooman/venuscloud/duelify-env/site/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/hooman/venuscloud/duelify-env/site/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/hooman/venuscloud/duelify-env/site/static_files/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'il8zx-az!ti=e-@m5u&amp;q54q%_%aidnfj05jq4#c8ldax!h3mn2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',    
    'django.middleware.transaction.TransactionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'duelify.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'duelify.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/hooman/venuscloud/duelify-env/site/templates/'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'widget_tweaks',
    'pipeline',
    'duelify_app',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
