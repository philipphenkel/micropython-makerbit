# MakerBit MicroPython Firmware for the BBC Micro:bit


## How to build the firmware

```bash
podman build -t micropython-makerbit .
podman run --name makerbit micropython-makerbit
podman cp makerbit:/microbit-micropython/build/firmware.hex makerbit-python.hex
```
