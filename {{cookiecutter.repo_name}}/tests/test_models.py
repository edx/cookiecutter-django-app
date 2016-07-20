#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the `{{ cookiecutter.repo_name }}` models module.
"""

from __future__ import absolute_import, unicode_literals{% if cookiecutter.models != "Comma-separated list of models" %}{% for model in cookiecutter.models.replace(' ', '').split(',') %}


class Test{{ model }}(object):
    """
    Tests of the {{ model }} model.
    """

    def test_something(self):
        """TODO: Write real test cases."""
        pass{% endfor %}{% endif %}
