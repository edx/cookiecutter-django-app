"""
URLs for {{ cookiecutter.sub_dir_name }}.
"""
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'', TemplateView.as_view(template_name="{{ cookiecutter.sub_dir_name }}/base.html")),
]
