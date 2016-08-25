Part of `edX code`__.

__ http://code.edx.org/

{{cookiecutter.project_name}}  |Travis|_ |Codecov|_
===================================================
.. |Travis| image:: https://travis-ci.org/edx/{{cookiecutter.repo_name}}.svg?branch=master
.. _Travis: https://travis-ci.org/edx/{{cookiecutter.repo_name}}

.. |Codecov| image:: http://codecov.io/github/edx/{{cookiecutter.repo_name}}/coverage.svg?branch=master
.. _Codecov: http://codecov.io/github/edx/{{cookiecutter.repo_name}}?branch=master

The ``README.rst`` file should start with a brief description of the repository,
which sets it in the context of other repositories under the ``edx``
organization. It should make clear where this fits in to the overall edX
codebase.

{{ cookiecutter.project_short_description}}

Overview (please modify)
------------------------

The ``README.rst`` file should then provide an overview of the code in this
repository, including the main components and useful entry points for starting
to understand the code in more detail.

Documentation
-------------

The full documentation is at https://{{ cookiecutter.repo_name }}.readthedocs.org.

License
-------

The code in this repository is licensed under the {{ cookiecutter.open_source_license }} unless
otherwise noted.

Please see ``LICENSE.txt`` for details.

How To Contribute
-----------------

Contributions are very welcome.

Please read `How To Contribute <https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details.

Even though they were written with ``edx-platform`` in mind, the guidelines
should be followed for Open edX code in general.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Mailing List and IRC Channel
----------------------------

You can discuss this code in the `edx-code Google Group`__ or in the ``#edx-code`` IRC channel on Freenode.

__ https://groups.google.com/forum/#!forum/edx-code
