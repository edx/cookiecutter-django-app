"""
These settings are here to use during tests, because django requires them.

In a real-world use case, apps in this project are installed into other
Django applications, so these settings will not be used.
"""

from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'default.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    '{{ cookiecutter.sub_dir_name }}',
)

LOCALE_PATHS = [
    root('{{ cookiecutter.sub_dir_name }}', 'conf', 'locale'),
]

ROOT_URLCONF = '{{ cookiecutter.sub_dir_name }}.urls'

SECRET_KEY = 'insecure-secret-key'
