import multiprocessing
import os

import djcelery

DIRNAME = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

ADMINS = ()

MANAGERS = ADMINS

TIME_ZONE = "America/New_York"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ""
MEDIA_URL = ""
IIIF_IMAGE_BASE_URL = None
REDIRECT_IMAGES_TO_IIIF = False

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.CachedStaticFilesStorage"

STATIC_URL = "/media/"
STATIC_ROOT = os.path.join(DIRNAME, ".static-media")

ROOT_URLCONF = "chronam.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "chronam",
        "USER": "chronam",
        "PASSWORD": "pick_one",
        "CONN_MAX_AGE": 300,
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = "px2@!q2(m5alb$0=)h@u*80mmf9cd-nn**^y4j2j&+_8h^n_0f"

# persist the database connections instead of closing after each request
CONN_MAX_AGE = None

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"},
        "simple": {"format": "[%(asctime)s %(levelname)s %(name)s] %(message)s"},
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": "/var/log/httpd/chronam.log",
            "maxBytes": 1024 * 1024 * 50,  # 50MB
            "backupCount": 5,
        },
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "simple"},
    },
    "root": {"handlers": ["file", "console"], "level": "INFO"},
}

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "chronam.core.middleware.TooBusyMiddleware",
    "chronam.core.middleware.CloudflareCacheHeader",
)


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(DIRNAME, "templates")],
        "OPTIONS": {
            "context_processors": [
                "chronam.core.context_processors.extra_request_info",
                "chronam.core.context_processors.site_navigation",
            ],
            "debug": DEBUG,
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                )
            ],
        },
    }
]


INSTALLED_APPS = (
    "django.contrib.humanize",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "djcelery",
    "kombu.transport.django",
    "chronam.core",
)

SITE_ID = 1

BROKER_URL = "django://"

THUMBNAIL_WIDTH = 360
THUMBNAIL_MEDIUM_WIDTH = 550

DEFAULT_TTL_SECONDS = 86400  # 1 day
LONG_TTL_SECONDS = DEFAULT_TTL_SECONDS
#: Used to cache metadata about publishers, issues, etc. as distinct from HTML
# pages, images, search results, etc.
METADATA_TTL_SECONDS = DEFAULT_TTL_SECONDS
PAGE_IMAGE_TTL_SECONDS = DEFAULT_TTL_SECONDS
API_TTL_SECONDS = 60 * 60  # 1 hour
SHARED_CACHE_MAXAGE_SECONDS = DEFAULT_TTL_SECONDS

USE_TIFF = False

ESSAYS_FEED = "https://essays.loc.gov/feed/"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
        "TIMEOUT": 4838400,  # 2 months
    }
}

IS_PRODUCTION = False

MAX_BATCHES = 0

SENDFILE_BACKEND = "sendfile.backends.xsendfile"
#: If set, instead of using Sendfile a redirect will be issued to the path
#: urljoin()-ed with this value
SENDFILE_REDIRECT_BATCH_BASE_URL = "https://chroniclingamerica.loc.gov/data/batches/"

TOO_BUSY_LOAD_AVERAGE = 1.5 * multiprocessing.cpu_count()
# TOO_BUSY_LOAD_AVERAGE = 64

SOLR = "http://localhost:8983/solr"
SOLR_LANGUAGES = (
    "ara",
    "cze",
    "dak",
    "dan",
    "eng",
    "fin",
    "fre",
    "ger",
    "hrv",
    "ice",
    "ita",
    "lit",
    "nob",
    "pol",
    "rum",
    "slo",
    "slv",
    "spa",
    "swe",
)

STORAGE = "/srv/chronam/"
BATCH_STORAGE = os.path.join(STORAGE, "batches")
BIB_STORAGE = os.path.join(STORAGE, "bib")
COORD_STORAGE = os.path.join(STORAGE, "word_coordinates")
OCR_DUMP_STORAGE = os.path.join(COORD_STORAGE, "ocr")
TEMP_STORAGE = "/opt/chronam/temp"  # because /tmp is often too small...

BASE_CRUMBS = [{"label": "Home", "href": "/"}]

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]


djcelery.setup_loader()
