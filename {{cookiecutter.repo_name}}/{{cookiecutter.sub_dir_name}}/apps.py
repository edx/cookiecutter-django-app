"""
{{ cookiecutter.sub_dir_name }} Django application initialization.
"""

from django.apps import AppConfig


class {{ cookiecutter.config_class_name }}(AppConfig):
    """
    Configuration for the {{ cookiecutter.sub_dir_name }} Django application.
    """

    name = '{{ cookiecutter.sub_dir_name }}'
