"""
Tests of the project generation output.
"""

from __future__ import absolute_import, print_function, unicode_literals

import logging.config
import os
import re
from contextlib import contextmanager

import pytest

import sh
from cookiecutter.utils import rmtree

LOGGING_CONFIG = {
    'version': 1,
    'incremental': True,
    'loggers': {
        'binaryornot': {
            'level': logging.INFO,
        },
        'sh': {
            'level': logging.INFO,
        }
    }
}
logging.config.dictConfig(LOGGING_CONFIG)


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory.

    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests.

    :param cookies: pytest_cookies.Cookies, cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def test_bake_selecting_license(cookies):
    """Test to check if LICENSE.txt gets the correct license selected."""
    license_strings = {
        'AGPL 3.0': 'GNU AFFERO GENERAL PUBLIC LICENSE',
        'Apache Software License 2.0': 'Apache',
    }
    for license_name, target_string in license_strings.items():
        with bake_in_temp_dir(cookies, extra_context={'open_source_license': license_name}) as result:
            assert target_string in result.project.join('LICENSE.txt').read()
            assert license_name in result.project.join('setup.py').read()


def test_readme(cookies):
    """The generated README.rst file should pass some sanity checks and validate as a PyPI long description."""
    extra_context = {'repo_name': 'helloworld'}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:

        readme_file = result.project.join('README.rst')
        readme_lines = [x.strip() for x in readme_file.readlines(cr=False)]
        assert 'helloworld' in readme_lines
        assert 'The full documentation is at https://helloworld.readthedocs.org.' in readme_lines
        setup_path = str(result.project.join('setup.py'))
        try:
            sh.python(setup_path, 'check', restructuredtext=True, strict=True)
        except sh.ErrorReturnCode as exc:
            pytest.fail(str(exc))


def test_models(cookies):
    """The generated models.py file should pass a sanity check."""
    extra_context = {'models': 'ChocolateChip, Zimsterne', 'app_name': 'cookies'}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:

        model_file = result.project.join('cookies', 'models.py')
        model_txt = model_file.read()
        for model_name in ['ChocolateChip', 'Zimsterne']:
            pattern = r'^class {}\(TimeStampedModel\):$'.format(model_name)
            assert re.search(pattern, model_txt, re.MULTILINE)


def test_urls(cookies):
    """The urls.py file should be present."""
    extra_context = {'app_name': 'cookies'}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:
        urls_file = result.project.join('cookies', 'urls.py')
        urls_file_txt = urls_file.read()
        basic_url = "url(r'', TemplateView.as_view(template_name=\"cookies/base.html\"))"
        assert basic_url in urls_file_txt


def test_travis(cookies):
    """The generated .travis.yml file should pass a sanity check."""
    extra_context = {'app_name': 'cookie_lover'}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:

        travis_file = result.project.join('.travis.yml')
        travis_text = travis_file.read()
        assert 'pip install -r requirements/travis.txt' in travis_text


def test_app_config(cookies):
    """The generated Django AppConfig should look correct."""
    extra_context = {'app_name': 'cookie_lover'}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:
        init_file = result.project.join('cookie_lover', '__init__.py')
        pattern = r"^default_app_config = 'cookie_lover.apps.CookieLoverConfig'  #"
        assert re.search(pattern, init_file.read(), re.MULTILINE)

        apps_file = result.project.join('cookie_lover', 'apps.py')
        pattern = r'^class CookieLoverConfig\(AppConfig\):$'
        assert re.search(pattern, apps_file.read(), re.MULTILINE)


def test_authors(cookies):
    """The generated AUTHORS file should contain the appropriate entry."""
    extra_context = {'full_name': 'Cookie McCookieface', 'email': 'cookie@edx.org'}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:

        authors_file = result.project.join('AUTHORS')
        authors_text = authors_file.read()
        assert 'Cookie McCookieface <cookie@edx.org>' in authors_text


def test_manifest(cookies):
    """The generated MANIFEST.in should pass a sanity check."""
    extra_context = {'app_name': 'cookie_lover'}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:

        manifest_file = result.project.join('MANIFEST.in')
        manifest_text = manifest_file.read()
        assert 'recursive-include cookie_lover *.html *.png *.gif *js *.css *jpg *jpeg *svg *py' in manifest_text


def test_setup_py(cookies):
    """The generated setup.py should pass a sanity check."""
    extra_context = {'app_name': 'cookie_lover', 'full_name': 'Cookie McCookieface'}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:

        setup_file = result.project.join('setup.py')
        setup_text = setup_file.read()
        assert "VERSION = get_version('cookie_lover', '__init__.py')" in setup_text
        assert "    author='edX'," in setup_text


def test_quality_without_models(cookies):
    """The generated project should pass quality checks when no models are specified."""
    with bake_in_temp_dir(cookies) as result:
        check_quality(result)


def test_quality_with_models(cookies):
    """The generated project should pass quality checks when models are specified."""
    extra_context = {'models': 'ChocolateChip,Zimsterne', 'app_name': 'cookies'}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:
        check_quality(result)


def check_quality(result):
    """Run quality tests on the given generated output."""
    for dirpath, _dirnames, filenames in os.walk(str(result.project)):
        pylintrc = str(result.project.join('pylintrc'))
        for filename in filenames:
            name = os.path.join(dirpath, filename)
            if not name.endswith('.py'):
                continue
            try:
                sh.pylint(name, rcfile=pylintrc)
                sh.pylint(name, py3k=True)
                sh.pycodestyle(name)
                if filename != 'setup.py':
                    sh.pydocstyle(name)
                sh.isort(name, check_only=True)
            except sh.ErrorReturnCode as exc:
                pytest.fail(str(exc))

    tox_ini = result.project.join('tox.ini')
    docs_build_dir = result.project.join('docs/_build')
    try:
        # Sanity check the generated Makefile
        sh.make('help')
        # quality check docs
        sh.doc8(result.project.join("README.rst"), ignore_path=docs_build_dir, config=tox_ini)
        sh.doc8(result.project.join("docs"), ignore_path=docs_build_dir, config=tox_ini)
    except sh.ErrorReturnCode as exc:
        pytest.fail(str(exc))
