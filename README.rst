Harbinger
=========

Abstract transport to connect to remote servers with performance in mind

.. image:: docs/source/images/logo_256.png

Installation
------------

.. code:: sh

   sudo apt-get install make
   python setup.py install

Examples
--------

Install the dependencies.

.. code:: sh

   pip install .[ssh2,paramiko]

Run one of the examples in the ``examples`` folder.

.. code:: sh

   env PYTHONPATH=$PYTHONPATH:$(pwd) examples/telnet_ls_shell.py

.. code::

   Configuring Telnet connection
   Hostname: localhost
   Port: 23
   Username: user
   Password:
   Creating Telnet connection object
   Connecting
   Sending 'ls'
   Receiving output
   bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
   boot  etc  lib   media  opt  root  sbin  sys  usr
   Disconnecting
   Done


Tests
-----

Install tests requirements.

.. code:: sh

   sudo apt-get install make
   pip install -r requirements/dev.txt

Run Nose and Flake 8.

.. code:: sh

   nosetests
   flake8 *.py harbinger docs

If you are running Python 3.6+, install and execute Black.

.. code:: sh

   pip install black

.. code:: sh

   black --exclude harbinger/execeptions.py --diff --check -l 79 *.py harbinger docs

Documentation
-------------

The documentation is available on ReadTheDocs: https://harbinger.readthedocs.io/en/latest/

Building the documentation
--------------------------

Install Sphinx requirements.

.. code:: sh

   sudo apt-get install make
   pip install sphinx

Run Sphinx.

.. code:: sh

   make -C docs html

The resulting HTML pages are available in `docs/build/html`.
