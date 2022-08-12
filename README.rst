=====
pimon
=====

Description
===========

IMAP4 proxy interface by Python.

Installation
============

.. code-block:: console

   curl -sSL -o install.py https://raw.githubusercontent.com/attakei-lab/pimon/main/scripts/install
   python install.py
   pimon init [--workspace=/PATH/TO/workspace]

Usage
=====

Edit ``/PATH/TO/WORKSPACE/accounts.ini`` before using.

.. code-block:: console

   pimon fetch
   pimon list
   pimon archive account-11111

Motivation
==========

See some emails (Gmail, Outlook and others) by **single** and **lightweight** interface.

Pimon is for ...
----------------

* Collect email header info to **list**
* Fech body content by manually
* Modify email as **archived easily**
* Cross reading multiple email-services

Pimon is not for ...
--------------------

* Email reader (This does not have high-spec viewer)
* Email sender (This does not have editor)

License
=======

Apache 2.0
