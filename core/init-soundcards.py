#!/usr/bin/env python3

import os, sys
import subprocess
import configparser

INI_FILE = "soundsys.ini"
CONF: configparser.ConfigParser
HUB: list


def find_usb_hub():
   hub_bus = CONF["hub"]["bus"]
   hub_usbid = CONF["hub"]["usbid"]
   print(f"hub_usbid: {hub_usbid}")
   res = subprocess.run(["lsusb", "-d", f"{hub_usbid}"], stdout=subprocess.PIPE)
   global HUB
   HUB = []
   for ln in res.stdout.decode("utf-8").split('\n'):
      ln = ln.strip()
      if ln != "":
         HUB.append(ln)
   print(HUB)
   # get bus id
   bus_id = ""


def find_sound_cards():
   scs_usbids = CONF["soundcards"]["usbids"]
   print(f"scs_usbids: {scs_usbids}")


def main():
   print("main")
   global CONF
   CONF = configparser.ConfigParser()
   CONF.read(INI_FILE)
   find_usb_hub()
   find_sound_cards()


# - - - start - - -
if __name__ == "__main__":
   main()
