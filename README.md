# KonkeIO
This library (and its accompanying cli tool) is used to interface with
Konke remote-control devices.

## Supported Devices

### Socket
- Mini K `minik`
- Mini Pro `minik`
- Smart Plug K(untested) `k1`
- K2 Pro `k2`

### Power Strip
- The normal one(untested) `micmul`
- The Standing one with USB support(untested) `mul`

### Light
- KLight (LED with RGB color) `klight`
- KBlum/K2Light `kbulb`

## Install

```bash
    pip install pykoneio
```

## API Reference

### classes and methods
- K2(ip)
    - online
    - status
    - update()
    - turn_on()
    - turn_off()
    - turn_on_usb()
    - turn_off_usb()
    - turn_on_light()
    - turn_off_light()
- MinkK(ip)
    - online
    - status
    - update()
    - turn_on()
    - turn_off()
- Mul(ip)
    - online
    - status[]
    - usb_status[]
    - update()
    - turn_on(index)
    - turn_off(index)
    - turn_on_all()
    - turn_off_all()
    - turn_on_usb(index)
    - turn_off_usb(index)
- MicMul(ip)
    - online
    - status[]
    - update()
    - turn_on(index)
    - turn_off(index)
    - turn_on_all()
    - turn_off_all()
- KLight(ip)
    - online
    - status
    - color
    - brightness
    - update()
    - turn_on()
    - turn_off()
    - set_color()
    - set_brightness()
- KBulb
    - online
    - status
    - ct
    - brightness
    - update()
    - turn_on()
    - turn_off()
    - set_ct()
    - set_brightness()

Demo:

```python

    from pykonkeio import K2

    k2 = K2('192.168.0.222')

    if not k2.online:
        print('switch is off line')
    if k2.status == 'open':
        k2.turn_off()
    elif k2.status == 'close':
        k2.turn_on()
```

## CLI Command

```bash
usage: konkeio [action] [device] [address] [value] [--verbose]

Supported devices and actions supported by each device:
global: search
k2:     get_status turn_[on/off] turn_[on/off]_usb turn_[on/off]_light
minik:  get_status turn_[on/off]
micmul: get_count get_status_all get_status[1/2/3/4] turn_[on/off]_all turn_[on/off]_socket[1/2/3/4]
mul:    get_count get_status_all get_status[1/2/3] get_usb_count get_usb_status_all get_usb_status[1/2]
        turn_[on/off]_all turn_[on/off]_socket[1/2/3] turn_[on/off]_usb[1/2]
klight: get_status get_brightness get_color turn_[on/off] set_brightness set_color
kbulb:  get_status get_brightness get_ct turn_[on/off] set_brightness set_ct

* each action starts with 'set_' must provide a value parameter
value format:
color:      r,g,b
ct:         2700-6500
brightness: 0-100

example:
konkeio search
konkeio turn_on minik 192.168.0.64
konkeio get_status minik 192.168.0.64
konkeio turn_on_usb k2 192.168.0.64
konkeio turn_off_light k2 192.168.0.64
konkeio get_count micmul 192.168.0.64
konkeio turn_on_socket3 micmul 192.168.0.64
konkeio get_status2 mul 192.168.0.64
konkeio turn_off_all mul 192.168.0.64
konkeio get_brightness klight 192.168.0.64
konkeio set_color klight 192.168.0.64 255,255,0
konkeio set_ct kbulb 192.168.0.64 3400
konkeio turn_off bulb 192.168.0.64
```