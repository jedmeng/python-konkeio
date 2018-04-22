This library (and its accompanying cli tool) is used to interface with Konke remote-control devices.

# Supported Devices

- Mini K
![Mini K](http://www.ikonke.com/pro/miniK/images/minik_img1.png)
- Mini Pro
![Mini Pro](https://img.alicdn.com/imgextra/i2/2259671767/TB2ZgLZi4rI8KJjy0FpXXb5hVXa_!!2259671767.jpg_430x430q90.jpg)
- Smart Plug K(untested)
![K](https://gd4.alicdn.com/imgextra/i4/322866315/TB2KOYpbgMPMeJjy1XcXXXpppXa_!!322866315.jpg_400x400.jpg_.webp)
- K2 Pro(untested)
![K2](https://img.alicdn.com/imgextra/i4/2259671767/TB2THHQtXXXXXcoXpXXXXXXXXXX_!!2259671767.jpg_430x430q90.jpg)

# Install
```bash
pip install pykone
```

# API Reference

- *class **Switch***(ip) create a instance of a switch
  - *check()* get switch's status
  - *turn_on()* turn on the switch
  - *turn_off()* turn off the switch
  
Demo: 
```python
from pykonke import Switch

switch = Switch('192.168.0.222')

if switch.status == 'open':
    switch.turn_off()
elif switch.status == 'close':
    switch.turn_on()
elif switch.status == 'offline':
    print('switch is off line')

```

# CLI Command

- search device
```bash
pykone search
```

- check device status
```bash
pykone check -a [device ip address]
```

- turn on switch
```bash
pykone open -a [device ip address]
```

- turn off switch
```bash
pykone close -a [device ip address]
```