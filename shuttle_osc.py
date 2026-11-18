#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 contributeurs de ShuttleOSC
# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["hidapi", "python-osc"]
# ///
"""Passerelle Contour ShuttleXpress -> OSC (pour Chataigne).

Messages envoyes :
  /shuttle/jog/up          (sans argument) : 1 message par cran du jog vers la droite
  /shuttle/jog/down        (sans argument) : 1 message par cran vers la gauche
  /shuttle/ring  <int>     : position de la bague a ressort, -7 a 7 (0 = repos)
  /shuttle/button/<n> <int>: 1 a l'appui, 0 au relachement (n = 1 a 5)

Usage : python shuttle_osc.py [--host 127.0.0.1] [--port 9000] [--debug]
"""
import argparse
import sys
import time

import hid
from pythonosc.udp_client import SimpleUDPClient

VENDOR_ID = 0x0B33              # Contour Design
PRODUCT_IDS = (0x0020,)         # ShuttleXpress (0x0030 = ShuttlePRO v2)


def signed8(b):
    return b - 256 if b > 127 else b


def open_device():
    for pid in PRODUCT_IDS:
        try:
            d = hid.device()
            d.open(VENDOR_ID, pid)
            return d
        except (IOError, OSError):
            continue
    return None


def button_numbers(mask):
    """Numerote les bits actifs du masque de boutons dans l'ordre (1, 2, 3...)."""
    return [i + 1 for i in range(16) if mask & (1 << i)]


class Bridge:
    def __init__(self, client, debug=False):
        self.osc = client
        self.debug = debug
        self.last_jog = None
        self.last_ring = 0
        self.last_buttons = 0
        self.bit_to_button = {}   # bit HID -> numero de bouton 1..5, appris dans l'ordre

    def send(self, address, *args):
        self.osc.send_message(address, list(args))
        if self.debug:
            print("OSC", address, *args)

    def button_index(self, bit):
        # ShuttleXpress : boutons attendus sur les bits 4,5,6,7 (octet 3) et 8 (octet 4)
        known = {4: 1, 5: 2, 6: 3, 7: 4, 8: 5}
        return known.get(bit, bit + 1)

    def handle(self, report):
        if len(report) < 5:
            return
        if self.debug:
            print("HID", " ".join("%02x" % b for b in report[:5]))

        # Bague shuttle (a ressort)
        ring = signed8(report[0])
        if ring != self.last_ring:
            self.send("/shuttle/ring", ring)
            self.last_ring = ring

        # Jog : compteur 0-255 qui boucle -> on calcule l'ecart signe
        jog = report[1]
        if self.last_jog is not None:
            delta = (jog - self.last_jog + 128) % 256 - 128
            address = "/shuttle/jog/up" if delta > 0 else "/shuttle/jog/down"
            for _ in range(abs(delta)):
                self.send(address)
        self.last_jog = jog

        # Boutons : octets 3 et 4
        buttons = report[3] | (report[4] << 8)
        changed = buttons ^ self.last_buttons
        for bit in range(16):
            if changed & (1 << bit):
                pressed = 1 if buttons & (1 << bit) else 0
                self.send("/shuttle/button/%d" % self.button_index(bit), pressed)
        self.last_buttons = buttons


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=9000)
    p.add_argument("--debug", action="store_true", help="affiche les donnees HID et OSC")
    a = p.parse_args()

    bridge = Bridge(SimpleUDPClient(a.host, a.port), a.debug)
    print("Envoi OSC vers %s:%d. Ctrl+C pour quitter." % (a.host, a.port))

    while True:
        dev = open_device()
        if dev is None:
            print("ShuttleXpress introuvable, nouvel essai dans 2 s...")
            time.sleep(2)
            continue
        print("ShuttleXpress connecte.")
        bridge.last_jog = None
        try:
            while True:
                report = dev.read(64, 1000)   # attente max 1 s
                if report:
                    bridge.handle(report)
        except (IOError, OSError) as e:
            print("Appareil deconnecte (%s)." % e)
        finally:
            try:
                dev.close()
            except Exception:
                pass
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
