# MakerBit MicroPython Firmware for the BBC Micro:bit 


## How to build the firmware

```bash
sudo podman build -t micropython-makerbit .
sudo podman run --name makerbit micropython-makerbit
sudo podman cp makerbit:/microbit-micropython/build/firmware.hex makerbit-python.hex
```
