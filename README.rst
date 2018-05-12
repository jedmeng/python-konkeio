This library (and its accompanying cli tool) is used to interface with
Konke remote-control devices.

Supported Devices
=================

-  Mini K
-  Mini Pro
-  Smart Plug K(untested)
-  K2 Pro(untested)
Install
=======

.. code-block:: bash

    pip install pykoneio

API Reference
=============

-  class **Switch** (ip) create a instance of a switch
-  *check()* get switch's status
-  *turn_on()* turn on the switch
-  *turn_off()* turn off the switch

Demo:

.. code-block:: python

    from pykonkeio import Switch

    switch = Switch('192.168.0.222')

    if switch.status == 'open':
        switch.turn_off()
    elif switch.status == 'close':
        switch.turn_on()
    elif switch.status == 'offline':
        print('switch is off line')

CLI Command
===========

-  search device

   .. code-block:: bash

       koneio search

-  check device status

   .. code-block:: bash

       koneio check -a [device ip address]

-  turn on switch

   .. code-block:: bash

       koneio open -a [device ip address]

-  turn off switch

   .. code-block:: bash

       koneio close -a [device ip address]
