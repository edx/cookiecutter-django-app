# -*- coding: utf-8 -*-
"""
{{ cookiecutter.app_name }} Django application initialization.
"""

from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class {{ cookiecutter.config_class_name }}(AppConfig):
    """
    Configuration for the {{ cookiecutter.app_name }} Django application.
    """

    name = '{{ cookiecutter.app_name }}'
