# Django settings for kwippyproject project.
ADMINS = (
    ('Dipankar', 'dipankar@kwippy.com'),
)

MANAGERS = ADMINS
DEFAULT_FROM_EMAIL= 'support@kwippy.com'
SERVER_EMAIL = 'support@kwippy.com'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

SECRET_KEY = '_j-rv&metasd8#!(uz6ve6*m(^!lvl92uw5-&kj##=qw4*k'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'kwippyproject.dual_session_middleware.DualSessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'kwippyproject.urls'
PERSISTENT_SESSION_KEY = 'sessionpersistent'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "kwippyproject.session_context_processor.flash",    
) 

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.admin',
    'django.contrib.markup', 
    #'django.contrib.sitemaps',
    'kwippyproject.signup_app',
    'kwippyproject.comm_queue_app',
    'kwippyproject.kwippy',
    'kwippyproject.dbmigration',
    'kwippyproject.countries',
    'kwippyproject.feedback_app',
    'kwippyproject.robots',
)

AWS_ACCESS_KEY_ID = '<>'
AWS_SECRET_ACCESS_KEY = '<>'
BUCKET_NAME = 'kwippy-test'
RESERVED_WORDS_LIST = ['site','blog','help','signup','login','home','dashboard','support','feedback','contactus','admin','explore','soap','xml', 'gdata', 'json', 'api', 'rss' ,'atom', 'anon' , 'anonymous', 'followers', 'following', 'kwip']

LOGIN_URL = '/login/'

AUTH_PROFILE_MODULE = 'kwippy.user_profile'

COMMENTS_ALLOW_PROFANITIES = True

AUTH_FILE = '/usr/local/nginx/adminpasswd'

# AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

# Virality API keys
VAKEY = '<>'
VSKEY = '<>'
VURL = 'http://virulant.com'

#length settings
MAX_LINE_BREAKS = 5
MAX_STR_LENGTH = 200

# Fireeagle keys
FE_CONSUMER_KEY = 'rLMeGcIHVV4V'
FE_CONSUMER_SECRET = 'PD5Cv6ibb1Qwe2vbNGMP6JK6H3kmaLUh'
FE_GENERAL_KEY = '7rfHlNPjMDGl'
FE_GENERAL_SECRET = 'ROdB1RlFbpBuQ2Fk0NkE6sJyogpGxhsu'

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

ROBOTS_SITEMAP_URL = "/sitemap.xml"

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_WAIT_TIMEOUT = 120
DATABASE_NAME = 'kwippy_staging'             # Or path to database file if using sqlite3.
DATABASE_USER = 'kwippy_user'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '3306'             # Set to empty string for default. Not used with sqlite3.

# Absolute path to the directory that holds media.	
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/staging/kwippyproject/public'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/public/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "http://www.kwippy.com/public/"

TEMPLATE_DIRS = (
    '/home/staging/kwippyproject/templates',
    '/usr/lib/python2.4/site-packages/django/contrib/admin/templates'
)

ACCOUNT_ACTIVATION_DAYS=60
#Caching stuff
#SESSION_CACHE = 'memcached://127.0.0.1:11200/'
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = 'main_'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'mailsender@kwippy.com'
#EMAIL_HOST_PASSWORD = '<>'
#EMAIL_PORT = 587

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

SPHINX_SERVER = '76.191.252.138'
SPHINX_PORT = 3312

REVISION_NUMBER = 104

SITE = "http://www.kwippy.com"

#SESSION_ENGINE = "kwippyproject.session_backend"

