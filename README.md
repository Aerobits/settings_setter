# settings_setter

Simple python script for automatic setting setup in Aerobits devices.

### Quickstart

1. Download the latest release from Github
2. Run the program:
   ```
   ./settings_setter --port /dev/ttyACM0 --file config.yaml > settings_programmed.txt
   ```
   You can redirect the stdout to a file to record the settings
   that were programmed into the device.
   The program will still comunicate using stderr.

### Config file format

```yaml
Config: # don't care. This field can be anything
  SETTINGS_DEFAULT: null # to transmit AT+SETTINGS_DEFAULT
  DRONE_ID_ADVERTISING_ENABLE: 0 # to transmit AT+DRONE_ID_ADVERTISING_ENABLE=0
  DRONE_ID_SCAN_ENABLE_WIFI: 1 # to transmit AT+DRONE_ID_SCAN_ENABLE_WIFI=1
```
