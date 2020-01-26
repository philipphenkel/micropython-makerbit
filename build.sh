#!/bin/sh

sudo podman build -t micropython-makerbit .
sudo podman rm makerbit || true
sudo podman run --name makerbit micropython-makerbit
sudo mkdir build
sudo podman cp makerbit:/microbit-micropython/build/firmware.hex build/makerbit-python.hex
sudo podman cp makerbit:/tmp/usedspace.txt build/makerbit-python-usedspace.txt
