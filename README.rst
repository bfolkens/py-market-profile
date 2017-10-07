========
Overview
========

.. image:: https://travis-ci.org/bfolkens/py-market-profile.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/bfolkens/py-market-profile

A library to calculate Market Profile (Volume Profile) from a Pandas DataFrame.  This library expects the DataFrame to have an index of ``timestamp`` and columns for each of the OHLCV values.


* Free software: BSD license

Installation
============

::

    pip install marketprofile

Example
=======

You can view a Jupyter notebook of an example here: `<examples/example.ipynb>`_

Documentation
=============

(Coming soon)

What is `Market Profile <http://eminimind.com/the-ultimate-guide-to-market-profile/>`_ and `How are these calculated <https://www.sierrachart.com/index.php?page=doc/StudiesReference/TimePriceOpportunityCharts.html#Calculations>`_?

Development
===========

To run the all tests run::

    tox
