# -*- coding: utf-8 -*-
"""
Database models for {{cookiecutter.app_name}}.
"""

from __future__ import absolute_import, unicode_literals

# from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from model_utils.models import TimeStampedModel

{% if cookiecutter.models != "Comma-separated list of models" %}

{% for model in cookiecutter.models.replace(' ', '').split(',') %}

@python_2_unicode_compatible
class {{ model.strip() }}(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.
    """

    # TODO: add field definitions

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return '<{{ model.strip() }}, ID: {}>'.format(self.id)
{% endfor %}{% endif %}
