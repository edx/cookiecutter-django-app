===========================
Cookiecutter Django Package
===========================

.. image:: https://travis-ci.org/edx/cookiecutter-django-app.svg?branch=master
    :target: https://travis-ci.org/edx/cookiecutter-django-app
    :alt: Travis

.. image:: https://img.shields.io/github/license/edx/cookiecutter-django-app.svg
    :target: https://github.com/edx/cookiecutter-django-app/blob/master/LICENSE.txt
    :alt: License

A cookiecutter_ template for creating reusable Django packages (installable apps) quickly.
If you're creating a standalone Django service, you should probably use
`cookiecutter-django-ida`_ instead.

**Why?** Creating reusable Django packages has always been annoying. There are no defined/maintained
best practices (especially for ``setup.py``), so you end up cutting and pasting hacky, poorly understood,
often legacy code from one project to the other. This template, inspired by `cookiecutter-djangopackage`_,
is designed to allow Django developers the ability to break free from cargo-cult configuration and follow
a common pattern dictated by the experts and maintained here.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _cookiecutter-django-ida: https://github.com/edx/cookiecutter-django-ida
.. _cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
.. _cookiecutter-djangopackage: https://github.com/pydanny/cookiecutter-djangopackage

Features
--------

* Sane setup.py for easy PyPI registration/distribution
* Travis-CI configuration
* Codecov configuration
* Tox configuration
* Sphinx Documentation
* AGPL licensed by default
* Basic model generation

Usage
------

First, create your empty repo on Github (in our example below, we would call
it ``blogging_for_humans``) and set up your virtual environment with your
favorite method.  To request a new repo in the ``edx`` organization,
`submit an ITSUPPORT ticket`_.  This ticket should also request that Travis
and Codecov be enabled for the new repository.

.. _submit an ITSUPPORT ticket: https://openedx.atlassian.net/servicedesk/customer/portal/1/create/50

**Note**: Your project will be created with README.rst file containing a pypi
badge, a travis-ci badge and a link to documentation on readthedocs.org. You
don't need to have these accounts set up before using Cookiecutter or
cookiecutter-django-app.

Now, get Cookiecutter_. Trust me, it's awesome::

    $ pip install cookiecutter

Now run it against this repo::

    $ cookiecutter https://github.com/edx/cookiecutter-django-app.git

You'll be prompted for some questions, answer them, then it will create a directory that is your new package.

Let's pretend you want to create a reusable Django app called "Blogging-for-Humans", with an app that can be placed
in ``INSTALLED_APPS`` as "blogging_for_humans". Rather than have to copy/paste from other people's projects and
then fight enthusiasm-destroying app layout issues like `setup.py` configuration and creating test
harnesses, you get Cookiecutter_ to do all the work.

**Warning**: After this point, change 'John Doe', 'jdoe@edx.org', etc. to your own information.

It prompts you for information that it uses to create the app, with defaults in square brackets. Answer them::

    Cloning into 'cookiecutter-django-app'...
    remote: Counting objects: 49, done.
    remote: Compressing objects: 100% (33/33), done.
    remote: Total 49 (delta 6), reused 48 (delta 5)
    Unpacking objects: 100% (49/49), done.
    full_name [Your full name here]: John Doe
    email [you@example.com]: jdoe@edx.org
    repo_name [blogging_for_humans]:
    app_name [blogging_for_humans]:
    project_name [dj-package]: Blogging-for-Humans
    project_short_description [Your project description goes here]: A sample Django package
    models [Comma-separated list of models]: Scoop, Flavor
    config_class_name [BloggingForHumansConfig]:
    version [0.1.0]:
    owner [edx/platform-team]:
    Select open_source_license:
    1 - AGPL
    2 - Apache Software License 2.0
    3 - Not open source
    Choose from 1, 2, 3 [1]:

Enter the project and take a look around::

    $ cd blogging_for_humans/
    $ ls

Generate a virtualenv and generate requirements files with dependencies
pinned to current versions (make sure you're using pip 7 or later)::

    $ mkvirtualenv Blogging-for-humans
    $ make upgrade

Create a GitHub repo and push it there::

    $ git init
    $ git add .
    $ git commit -m "first awesome commit"
    $ git remote add origin git@github.com:edx/blogging_for_humans.git
    $ git push -u origin master

Now take a look at your repo. Awesome, right?

It's time to write the code!!!

Running Tests
~~~~~~~~~~~~~~~~~

Code has been written, but does it actually work? Let's find out!

::

    workon <YOURVIRTUALENV>
    (myenv) $ make requirements
    (myenv) $ make test-all

Register on PyPI
~~~~~~~~~~~~~~~~~

Once you have at least a prototype working and tests running, it's time to
register the application on PyPI.  `Open an IT General Request ticket`_ to do
this, providing:

* The URL of the package's GitHub repository (ask for the ``deploy`` entry in
  ``.travis.yml`` to be updated)
* The `PyPI registration URL`_
* The ``PKG-INFO`` file generated by running ``python setup.py egg_info``.

This avoids the need to distribute the password for the edx PyPI account too
widely.

.. _Open an IT General Request ticket: https://openedx.atlassian.net/servicedesk/customer/portal/1/create/7
.. _PyPI registration URL: https://packaging.python.org/distributing/#register-your-project

Releasing on PyPI
~~~~~~~~~~~~~~~~~

Time to release a new version? Update the version number in the application
module's ``__init__.py`` file, update ``CHANGELOG.rst`` accordingly, and run::

    $ python setup.py tag


Add to Django Packages
~~~~~~~~~~~~~~~~~~~~~~~

Once you have a release, and assuming you have an account there, just go to https://www.djangopackages.com/packages/add/ and add it there.


License
-------

The code in this repository is licensed under the Apache License, Version 2.0,
unless otherwise noted.

Please see ``LICENSE.txt`` for details.


How to Contribute
-----------------

Contributions are very welcome. The easiest way is to fork this repo, and then
make a pull request from your fork. The first time you make a pull request, you
may be asked to sign a Contributor Agreement.


Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org

Getting Help
------------

Have a question about this repository, or about Open edX in general?  Please
refer to this `list of resources`_ if you need any assistance.

.. _list of resources: https://open.edx.org/getting-help
