"""
{{ cookiecutter.project_short_description }}.
"""

from __future__ import absolute_import, unicode_literals

__version__ = '{{ cookiecutter.version }}'

default_app_config = '{{ cookiecutter.app_name }}.apps.{{ cookiecutter.config_class_name }}'  # pylint: disable=invalid-name
