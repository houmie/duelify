# Django settings for duelify project.

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
#LOGIN_ERROR_URL    = '/error'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-invited/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/login-invited/'
SIGNUP_ERROR_URL = '/signup-error/'
LOGIN_ERROR_URL = '/signup-error/'
SOCIAL_AUTH_USER_MODEL = 'duelify_app.User'

TWITTER_CONSUMER_KEY         = 'xxxx'
TWITTER_CONSUMER_SECRET      = 'xxxx'
FACEBOOK_APP_ID  = 'xxx'
FACEBOOK_API_SECRET = 'xxxx'
FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'user_birthday', 'user_location']
#FACEBOOK_EXTRA_DATA = [('user_birthday', 'user_location')]
GOOGLE_OAUTH2_CLIENT_ID = 'xxxx'
GOOGLE_OAUTH2_CLIENT_SECRET = 'xxxx'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False
#SOCIAL_AUTH_RAISE_EXCEPTIONS = True

AUTH_USER_MODEL = 'duelify_app.User'

SITE_HOST = 'duelify.com:8000'
DEFAULT_FROM_EMAIL = 'info@duelify.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'info@duelify.com'
EMAIL_HOST_PASSWORD = 'xxxxxx'
EMAIL_USE_TLS = True
SERVER_EMAIL = 'info@duelify.com'
EMAIL_SUBJECT_PREFIX = '[duelify]'

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

GEOIP_PATH = '/home/hooman/venuscloud/duelify-env/site/database/'
#GEOS_LIBRARY_PATH = '/opt/geos/lib/libgeos_c.so'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Hooman', 'xxx@xxx.com'),
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
    'social_buttons_css': {
        'source_filenames': (
          'css-social-buttons/css/zocial.css',
        ),
        'output_filename': 'css-social-buttons/css/zocial.min.css',        
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
    'ajaxform_js': {
        'source_filenames': (
          'ajaxform/jquery.form.js',
        ),
        'output_filename': 'ajaxform/jquery.form.min.js',
    },
}


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['duelify.com', 'www.duelify.com', '54.225.168.25']

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

#TINYMCE_JS_URL = STATIC_URL + 'tinymce/js/tinymce/tinymce.min.js'
#TINYMCE_JS_URL = '/home/hooman/venuscloud/duelify-env/site/static_files/tinymce/js/tinymce/tinymce.min.js' 
#TINYMCE_JS_ROOT = STATIC_ROOT + 'tinymce/js/tinymce'
#TINYMCE_JS_ROOT = '/home/hooman/venuscloud/duelify-env/site/static_files/tinymce/js/tinymce'
TINYMCE_COMPRESSOR = True
TINYMCE_DEFAULT_CONFIG = {
    # General options
    'mode' : "textareas",
    'theme' : "advanced",
    'plugins' : "media,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,wordcount,advlist,autosave",

#    'plugins': "spellchecker,directionality,paste,searchreplace",
#    'language': "{{ language }}",
#    'directionality': "{{ directionality }}",
#    'spellchecker_languages' : "{{ spellchecker_languages }}",
#    'spellchecker_rpc_url' : "{{ spellchecker_rpc_url }}",
    'theme_advanced_buttons1_add' : "media",
    'theme_advanced_buttons2_add' : "advimage",
    
    # Theme options
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,fontselect,fontsizeselect,", #fullscreen,code",
    'theme_advanced_buttons2' : "bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,|,forecolor,backcolor",
    #'theme_advanced_buttons3' : "tablecontrols,|,hr,sub,sup,|,charmap",

    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_statusbar_location' : "bottom",
    'theme_advanced_resizing' : 'true',

    #Example content CSS (should be your site CSS)
    #content_css : "/css/style.css",

    'template_external_list_url' : "lists/template_list.js",
    'external_link_list_url' : "lists/link_list.js",
    'external_image_list_url' : "lists/image_list.js",
    'media_external_list_url' : "lists/media_list.js",

    # Style formats
    'style_formats' : [
        {'title' : 'Bold text', 'inline' : 'strong'},
        {'title' : 'Red text', 'inline' : 'span', 'styles' : {'color' : '#ff0000'}},
        {'title' : 'Help', 'inline' : 'strong', 'classes' : 'help'},
        {'title' : 'Table styles'},
        {'title' : 'Table row 1', 'selector' : 'tr', 'classes' : 'tablerow'}
    ],

    'width': '700',
    'height': '400'
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'il8zx-az!ti=e-@m5u&amp;q54q%_%aidnfj05jq4#c8ldax!h3mn2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

AUTHENTICATION_BACKENDS = ('social_auth.backends.facebook.FacebookBackend',
                           'social_auth.backends.google.GoogleOAuth2Backend',
                           'social_auth.backends.twitter.TwitterBackend',
                           'django.contrib.auth.backends.ModelBackend',)

#TEMPLATE_CONTEXT_PROCESSORS = (
#    "django.contrib.auth.context_processors.auth",
#    "django.core.context_processors.debug",
#    "django.core.context_processors.i18n",
#    "django.core.context_processors.media",
#    "django.core.context_processors.static",
#    "django.core.context_processors.tz",
#    "django.contrib.messages.context_processors.messages",    
#    "django.core.context_processors.request",    
#    'social_auth.context_processors.social_auth_by_name_backends',
#    'social_auth.context_processors.social_auth_backends',
#    'social_auth.context_processors.social_auth_by_type_backends',
#    'social_auth.context_processors.social_auth_login_redirect',
#)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',    
    'django.middleware.transaction.TransactionMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',

    'duelify_app.utils.social_media_save',
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
    'tinymce',
    'pipeline',
    'south',
    'django.contrib.sitemaps',
    'social_auth',
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
