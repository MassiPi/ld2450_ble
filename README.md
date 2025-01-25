# ld2450_ble
Home assistant integration for LD2450 presence sensor ove Bluetooth

Home Assistant has an official integration for Hi-Link LD2410 distance sensor over Bluetooth (https://www.home-assistant.io/integrations/ld2410_ble/)

This is based on a python class managing sensor connection and data (https://github.com/930913/ld2410-ble)

The newer LD2450 also publishes data over bluetooth, so i modified the python class and the integration code to manage it.

Eventually, it works

The sensor only outputs coordinates of up to three targets and their speed, but those are not much useful so a big part of the available sensors in HA are calculated (distance, angle, moving, presence..)

![image](https://github.com/MassiPi/ld2450_ble/assets/2384381/7c8f944a-35a3-4fd5-a7cb-4913463a8ff2)

The LD2450 is also fully controllable over BLE, so i added switch (for multi-target mode), button (for reboot), select (for area mode) and number slider (for up to 3 areas configuration).

![image](https://github.com/MassiPi/ld2450_ble/assets/2384381/38e1a29c-66a0-4be3-83dd-ece0a1f10fc4)

I assume the code will be full of errors and could be written much better, but writing a custom integration in HA is a nightmare and this is far beyond what i thought i could do..

As a bonus, there is the 3d model for a sensor case (just print it..) (5 parts: sensor box (with text), back plate, 3-pieces-support to allow solid positioning of the sensor)

![image](https://github.com/user-attachments/assets/d84e66ad-e7e6-463b-be1d-7ceca93e85db)
