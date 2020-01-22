========================
Carson Living Python API
========================

.. image:: https://travis-ci.org/rado0x54/python-carson-living.svg?branch=master
    :target: https://travis-ci.org/rado0x54/python-carson-living

.. image:: https://coveralls.io/repos/github/rado0x54/python-carson-living/badge.svg?branch=master
    :target: https://coveralls.io/github/rado0x54/python-carson-living?branch=master

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0

Python Carson Living is a library written in Python that exposes the carson.live devices as Python objects.

Installation
------------

Carson Living Python should work against **Python 2.x >= 2.7** and **Python 3.x >= 3.5**.

Development Notes
-----------------
Request Headers
~~~~~~~~~~~~~~~
The library currently works with the following base headers:

.. code-block::

    User-Agent: Carson/1.0.171 (live.carson.app; build:245; iOS 13.1.0) Alamofire/1.0.171
    X-Device-Type: ios
    X-App-Version: 1.0.171(245)

Code Documentation
~~~~~~~~~~~~~~~~~~
The code follow the `Google Python Styleguide <https://google.github.io/styleguide/pyguide.html>`_ for docstring.

Git Branching Strategy
~~~~~~~~~~~~~~~~~~~~~~
This project uses `gitflow <https://nvie.com/posts/a-successful-git-branching-model/>`_ as a git branching model.



License
-------

python-carson-living is released under the Apache License Version 2.0. See the LICENSE_ file for more
details.

Credits && Thanks
-----------------

* A lot of the project setup and the API object design was inspired / launched off  https://github.com/tchellomello/python-ring-doorbell. Saved me a lot of headaches with tox, setuptools and Travis!.
