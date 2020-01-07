"""
Tests of the project generation output.
"""

import logging
import logging.config
import os
import re
from contextlib import contextmanager
from pathlib import Path

import pytest
import sh

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
    Bake a cookiecutter, and switch into the resulting directory.

    :param cookies: pytest_cookies.Cookies, cookie to be baked.
    """
    result = cookies.bake(*args, **kwargs)
    with inside_dir(str(result.project)):
        yield


def test_bake_selecting_license(cookies):
    """Test to check if LICENSE.txt gets the correct license selected."""
    license_strings = {
        'AGPL 3.0': 'GNU AFFERO GENERAL PUBLIC LICENSE',
        'Apache Software License 2.0': 'Apache',
    }
    for license_name, target_string in license_strings.items():
        with bake_in_temp_dir(cookies, extra_context={'open_source_license': license_name}):
            assert target_string in Path("LICENSE.txt").read_text()
            assert license_name in Path("setup.py").read_text()


def test_readme(cookies):
    """The generated README.rst file should pass some sanity checks and validate as a PyPI long description."""
    extra_context = {'repo_name': 'helloworld'}
    with bake_in_temp_dir(cookies, extra_context=extra_context):

        readme_file = Path('README.rst')
        readme_lines = [x.strip() for x in readme_file.open()]
        assert 'helloworld' in readme_lines
        assert 'The full documentation is at https://helloworld.readthedocs.org.' in readme_lines
        try:
            sh.python("setup.py", 'check', restructuredtext=True, strict=True)
        except sh.ErrorReturnCode as exc:
            pytest.fail(str(exc))


def test_models(cookies):
    """The generated models.py file should pass a sanity check."""
    extra_context = {'models': 'ChocolateChip, Zimsterne', 'app_name': 'cookies'}
    with bake_in_temp_dir(cookies, extra_context=extra_context):

        model_txt = Path("cookies/models.py").read_text()
        for model_name in ['ChocolateChip', 'Zimsterne']:
            pattern = r'^class {}\(TimeStampedModel\):$'.format(model_name)
            assert re.search(pattern, model_txt, re.MULTILINE)


def test_urls(cookies):
    """The urls.py file should be present."""
    extra_context = {'app_name': 'cookies'}
    with bake_in_temp_dir(cookies, extra_context=extra_context):
        urls_file_txt = Path("cookies/urls.py").read_text()
        basic_url = "url(r'', TemplateView.as_view(template_name=\"cookies/base.html\"))"
        assert basic_url in urls_file_txt


def test_travis(cookies):
    """The generated .travis.yml file should pass a sanity check."""
    extra_context = {'app_name': 'cookie_lover'}
    with bake_in_temp_dir(cookies, extra_context=extra_context):

        travis_text = Path(".travis.yml").read_text()
        assert 'pip install -r requirements/travis.txt' in travis_text


def test_app_config(cookies):
    """The generated Django AppConfig should look correct."""
    extra_context = {'app_name': 'cookie_lover'}
    with bake_in_temp_dir(cookies, extra_context=extra_context):
        init_text = Path("cookie_lover/__init__.py").read_text()
        pattern = r"^default_app_config = 'cookie_lover.apps.CookieLoverConfig'  #"
        assert re.search(pattern, init_text, re.MULTILINE)

        apps_text = Path("cookie_lover/apps.py").read_text()
        pattern = r'^class CookieLoverConfig\(AppConfig\):$'
        assert re.search(pattern, apps_text, re.MULTILINE)


def test_manifest(cookies):
    """The generated MANIFEST.in should pass a sanity check."""
    extra_context = {'app_name': 'cookie_lover'}
    with bake_in_temp_dir(cookies, extra_context=extra_context):

        manifest_text = Path("MANIFEST.in").read_text()
        assert 'recursive-include cookie_lover *.html *.png *.gif *js *.css *jpg *jpeg *svg *py' in manifest_text


def test_setup_py(cookies):
    """The generated setup.py should pass a sanity check."""
    extra_context = {'app_name': 'cookie_lover', 'full_name': 'Cookie McCookieface'}
    with bake_in_temp_dir(cookies, extra_context=extra_context):

        setup_text = Path("setup.py").read_text()
        assert "VERSION = get_version('cookie_lover', '__init__.py')" in setup_text
        assert "    author='edX'," in setup_text


def test_quality_without_models(cookies):
    """The generated project should pass quality checks when no models are specified."""
    with bake_in_temp_dir(cookies):
        check_quality()


def test_quality_with_models(cookies):
    """The generated project should pass quality checks when models are specified."""
    extra_context = {'models': 'ChocolateChip,Zimsterne', 'app_name': 'cookies'}
    with bake_in_temp_dir(cookies, extra_context=extra_context):
        check_quality()


def check_quality():
    """Run quality tests on the given generated output."""
    for dirpath, _dirnames, filenames in os.walk("."):
        for filename in filenames:
            name = os.path.join(dirpath, filename)
            if not name.endswith('.py'):
                continue
            try:
                sh.pylint(name)
                sh.pycodestyle(name)
                sh.pydocstyle(name)
                sh.isort(name, check_only=True, diff=True)
            except sh.ErrorReturnCode as exc:
                pytest.fail(str(exc))

    try:
        # Sanity check the generated Makefile
        sh.make('help')
        # quality check docs
        sh.doc8("README.rst", ignore_path="docs/_build")
        sh.doc8("docs", ignore_path="docs/_build")
    except sh.ErrorReturnCode as exc:
        pytest.fail(str(exc))


@pytest.mark.parametrize(
    "extra_context",
    [
        {},  # No models to generate.
        {'models': 'ChocolateChip,Zimsterne', 'app_name': 'cookies'},  # Two models to generate
    ],
)
def test_pii_annotations(cookies, extra_context):
    """
    Test that the pii_check make target works correctly.
    """
    with bake_in_temp_dir(cookies, extra_context=extra_context):
        try:
            sh.make('upgrade')  # first run make upgrade to populate requirements/test.txt
            sh.make('pii_check')
        except sh.ErrorReturnCode as exc:
            # uncovered models are expected IFF we generated any models via the cookiecutter.
            expected_uncovered_models = 0
            if 'models' in extra_context:
                # count the number of (unannotated) models the cookiecutter should generate.
                expected_uncovered_models = len(extra_context['models'].split(','))
            expected_message = 'Coverage found {} uncovered models:'.format(expected_uncovered_models)
            if expected_message not in str(exc.stdout):
                # First, print the stdout/stderr attrs, otherwise sh will truncate the output
                # guaranteeing that all we see is useless tox setup.
                print(exc.stdout)
                print(exc.stderr)
                pytest.fail(str(exc))
