# -*- coding: utf-8 -*-
"""
Database models for {{cookiecutter.app_name}}.
"""{% if cookiecutter.models != "Comma-separated list of models" %}
# from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel
{% for model in cookiecutter.models.replace(' ', '').split(',') %}

@python_2_unicode_compatible
class {{ model.strip() }}(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """

    # TODO: add field definitions

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return '<{{ model.strip() }}, ID: {}>'.format(self.id)
{% endfor %}{%else %}
{% endif %}