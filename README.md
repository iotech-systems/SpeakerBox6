# speakerbox6

add file 98-soudbox6.rules to folder: /lib/udev/rules.d

with this conntent:

SUBSYSTEM!="sound", GOTO="soundbox6_usb_audio_end"
ACTION!="add", GOTO="soundbox6_usb_audio_end"

DEVPATH=="/devices/pci0000:00/0000:00:10.0/usb5/5-2/5-2.1/5-2.1:1.0/sound/card?", ATTR{id}="SB6_P0"
DEVPATH=="/devices/pci0000:00/0000:00:10.0/usb5/5-2/5-2.2/5-2.2:1.0/sound/card?", ATTR{id}="SB6_P1"
DEVPATH=="/devices/pci0000:00/0000:00:10.0/usb5/5-2/5-2.3/5-2.3:1.0/sound/card?", ATTR{id}="SB6_P2"
DEVPATH=="/devices/pci0000:00/0000:00:10.0/usb5/5-2/5-2.4/5-2.4.1/5-2.4.1:1.0/sound/card?", ATTR{id}="SB6_P3"
DEVPATH=="/devices/pci0000:00/0000:00:10.0/usb5/5-2/5-2.4/5-2.4.2/5-2.4.2:1.0/sound/card?", ATTR{id}="SB6_P4"
DEVPATH=="/devices/pci0000:00/0000:00:10.0/usb5/5-2/5-2.4/5-2.4.3/5-2.4.3:1.0/sound/card?", ATTR{id}="SB6_P5"

LABEL="soundbox6_usb_audio_end"

