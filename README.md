# Parking sensor

The code in this project is designed for an RP2040.

# Usage

For help with `circup`, visit https://github.com/adafruit/circup

## device

1. Connect a device.

## build

1. Download the circuit python libraries

```
pip install -r requirements.txt
```

## deploy to device

```
circup install --auto
```

The File Watcher extension monitors file change events (On Save) and then copies the contents to the attached device. Change the device ID `F:` in your `.vscode/settings.json` file to the device ID for your connected device.
