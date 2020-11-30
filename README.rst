==============
Market Profile
==============

.. image:: https://api.travis-ci.org/bfolkens/py-market-profile.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/bfolkens/py-market-profile

.. image:: https://readthedocs.org/projects/marketprofile/badge/?version=latest
    :target: https://marketprofile.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


A library to calculate Market Profile (Volume Profile) from a Pandas DataFrame.  This library expects the DataFrame to have an index of ``timestamp`` and columns for each of the OHLCV values.


* Free software: BSD license

Installation
============

::

    pip install marketprofile

Example
=======

You can view a Jupyter notebook of an example with charts here: `<https://github.com/bfolkens/py-market-profile/blob/master/examples/example.ipynb>`_

Pull in some data to play with:

   >>> from market_profile import MarketProfile
   >>> import pandas_datareader as data
   >>> amzn = data.get_data_yahoo('AMZN', '2019-12-01', '2019-12-31')

Create the MarketProfile object from a Pandas DataFrame:

   >>> mp = MarketProfile(amzn)
   >>> mp_slice = mp[amzn.index.min():amzn.index.max()]

Once you've chosen a slice, you can return the profile series:

   >>> mp_slice.profile
   Close
   1739.25    2514300
   1740.50    2823800
   1748.75    2097600
   1749.55    2442800
   1751.60    3117400
   1760.35    3095900
   1760.70    2670100
   1760.95    2745700
   1769.25    3145200
   1770.00    3380900
   1781.60    3925600
   1784.05    3351400
   1786.50    5150800
   1789.25     881300
   1790.70    3644400
   1792.30    2652800
   1793.00    2136400
   1846.90    3674700
   1847.85    2506500
   1868.80    6005400
   1869.85    6186600
   Name: Volume, dtype: int64

Or you can also access individual attributes and properties:

   >>> mp_slice.initial_balance()
   (1762.680054, 1805.550049)

   >>> mp_slice.open_range()
   (1762.680054, 1805.550049)

   >>> mp_slice.poc_price
   1869.850000

   >>> mp_slice.profile_range
   (1739.25, 1869.85)

   >>> mp_slice.value_area
   (1760.95, 1869.85)

   >>> mp_slice.balanced_target
   2000.4499999999998

   >>> mp_slice.low_value_nodes
   Close
   1748.75    2097600
   1760.70    2670100
   1784.05    3351400
   1789.25     881300
   1793.00    2136400
   1847.85    2506500
   Name: Volume, dtype: int64

   >>> mp_slice.high_value_nodes
   Close
   1740.5    2823800
   1751.6    3117400
   1781.6    3925600
   1786.5    5150800
   1790.7    3644400
   1846.9    3674700
   Name: Volume, dtype: int64


Documentation
=============

https://marketprofile.readthedocs.io/

What is `Market Profile <https://eminimind.com/the-ultimate-guide-to-market-profile/>`_ and `How are these calculated <https://www.sierrachart.com/index.php?page=doc/StudiesReference/TimePriceOpportunityCharts.html#Calculations>`_?

A discussion on the difference between TPO (Time Price Opportunity) and VOL (Volume Profile) chart types:
`<https://jimdaltontrading.com/tpo-vs-volume-profile>`_

Development
===========

To run the all tests run::

    tox

Development sponsored in part by Cignals, LLC. - Bitcoin `Order Flow and Footprint Charts <https://cignals.io/>`_.

