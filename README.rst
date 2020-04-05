===============
bozbo
===============

Fast Fake API with simple setup using CFG files.


Install and usage
===================
Install bozbo 

.. code-block:: bash

    $ pip3 install git+https://github.com/gutierri/bozbo

Create a file routes.cfg with:

.. code-block:: cfg

    [my-endpoint]
    methods = get
    response = name
               address

Running:

.. code-block:: bash

    $ bozbo
    Bottle v0.12.16 server starting up (using WSGIRefServer())...
    Listening on http://localhost:8080/
    Hit Ctrl-C to quit

To receive JSON response, just access **localhost:8080/my-endpoint**
