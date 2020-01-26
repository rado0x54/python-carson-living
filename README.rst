========================
Carson Living Python API
========================

.. image:: https://badge.fury.io/py/carson-living.svg
    :target: https://badge.fury.io/py/carson-living

.. image:: https://travis-ci.org/rado0x54/python-carson-living.svg?branch=master
    :target: https://travis-ci.org/rado0x54/python-carson-living

.. image:: https://coveralls.io/repos/github/rado0x54/python-carson-living/badge.svg?branch=master
    :target: https://coveralls.io/github/rado0x54/python-carson-living?branch=master

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0

.. image:: https://img.shields.io/pypi/pyversions/carson-living.svg
    :target: https://pypi.python.org/pypi/carson-living

Python Carson Living is a library written in Python that exposes the carson.live devices as Python objects.

Please note, that `Carson <https://carson.live>`_ does not provide an official API documentation, therefore this project
is solely based on reverse engineering.

Getting started
---------------
Installation
~~~~~~~~~~~~~

Carson Living Python should work against **Python 2.x >= 2.7** and **Python 3.x >= 3.5**.

.. code-block::

    # Installing from PyPi
    $ pip install carson_living

    # Installing latest development
    $ pip install \
        git+https://github.com/rado0x54/python-carson-living@master

Initialize a Carson API object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Initializing an API object
    carson = Carson("account@email.com", 'your password')
    print(carson.user)
    # >> Martin
    print(carson.token)
    # >> ey...

You are also able to pass a valid JWT token during initialization which would prevent a login action as long as the token is valid:

.. code-block:: python

    # Initializing an API object with a valid token
    carson = Carson("account@email.com", 'your password', 'ey....')
    print(carson.token)
    # >> Martin

Since Carson Living uses JWT token with very long validity, it is recommended to save the active token via
``carson.token``, whenever one needs to reinitialize the API later on. The API library is robust to handle expired
JWT tokens (and 401 handling), so no need to check before.

Carson entities
~~~~~~~~~~~~~~~
The library currently supports the following entities and actions.

- User (``carson.user``): read
- Building (``carson.buildings``): read
- Doors (``building.doors``): read, open
- Cameras (``building.cameras``): read, images, video

Door entities
~~~~~~~~~~~~~
Doors can be "buzzed" open via ``door.open()``

.. code-block:: python

    # Open all Unit Doors of Main Building
    for door in carson.first_building.doors:
        if door.is_unit_door:
            print('Opening Unit Door {}'.format(door.name))
            door.open()

Camera entities
~~~~~~~~~~~~~~~
Eagle Eye cameras can produce live images and videos but also allow access to passed recordings (see API). The API can download the image and video directly into a provided file object
or just pass a generated url with an eagle_eye auth key ``A=c000....``. Please note, that the url can only be accessed as long as the ``auth_key`` is valid. Therefore it may make sense to
force the eagle eye api to refresh the auth key before generating a image or video url.

- Directly save a live image:

.. code-block:: python

        for camera in building.cameras:
            with open('image_{}.jpeg'.format(camera.entity_id), 'wb') as file:
                camera.get_image(file)

- Directly save a live video of 10s:

.. code-block:: python

        for camera in building.cameras:
            with open('video_{}.flv'.format(camera.entity_id), 'wb') as file:
                camera.get_video(file, timedelta(seconds=10))

- Directly download a image from a timestamp:

.. code-block:: python

    three_hours_ago = datetime.utcnow() - timedelta(hours=3)
    # download all images from 3 hours ago
    for camera in building.cameras:
        with open('image_{}.jpeg'.format(camera.entity_id), 'wb') as file:
            camera.get_image(file, three_hours_ago)

- Directly download a recorded video from a timestamp:

.. code-block:: python

        three_days_ago = datetime.utcnow() - timedelta(days=3)
        # download all videos from 3 days ago
        for cam in building.cameras:
            with open('video_{}.flv'.format(cam.entity_id), 'wb') as file:
                cam.get_video(file, timedelta(seconds=5), three_days_ago)

- The Carson API is also able to produce authenticated URLs that can be handled externally.
  Please not, that the ``auth_key`` has a limited lifetime. Therefore it makes sense to update
  the ``auth_key`` manually before retrieving predefined URLs. Note, the Eagle Eye API in Carson
  is associated with a building, so it is sufficient to update it once for all cameras in the same
  building. The function signature of the the ``_url`` function is identical to the previous ones
  (minus the file object).

.. code-block:: python

        # Update Session Auth Key of Eagle Eye once in a while if using
        # generated authenticated URLs.
        # Note, this is not needed for get_image() or get_video()
        building.eagleeye_api.update_session_auth_key()
        for cam in building.cameras:
            img_url = cam.get_image_url(three_days_ago)
            print(img_url)
            # >> https://cXXX.eagleeyenetworks.com/asset/prev/image.jpeg?id=c0&timestamp=20200122211442.575&asset_class=pre&A=c000~...
            response = requests.get(img_url)
            with open('image_{}_with_url.jpeg'.format(cam.entity_id), 'wb') as file:
                file.write(response.content)
            # do only 1 cam.
            break

Use ``cam.get_video_url()`` the same way.

CLI Tool
~~~~~~~~
Checkout ``./scripts/carsoncli.py`` for further API implementation examples.

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

Open Items
~~~~~~~~~~
The following is not supported by the API yet and remains TODO.

- Expose visitor functionality (``/visitors``)
- Expose thread / messaging functionality (``/threads``)
- Expose delivery functionality (``/deliveries``)
- Expose dashboard functionality (``/dashboard``)
- Expose service functionality (``/service``)
- Integrate Twilio (``twilio/access-token/``)
- Expand and extract EagleEye API (into separate project?).



License
-------

python-carson-living is released under the Apache License Version 2.0. See the LICENSE_ file for more
details.

Credits && Thanks
-----------------

* A lot of the project setup and the API object design was inspired / launched off  https://github.com/tchellomello/python-ring-doorbell. Saved me a lot of headaches with tox, setuptools and Travis!.
