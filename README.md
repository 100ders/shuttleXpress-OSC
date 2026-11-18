# ShuttleOSC

🇫🇷 Passerelle USB → OSC pour le **Contour ShuttleXpress** : jog, bague et 5 boutons envoyés en OSC vers n'importe quel logiciel (Châtaigne, TouchDesigner, Max, QLab, Isadora…).

🇬🇧 USB → OSC bridge for the **Contour ShuttleXpress**: jog wheel, shuttle ring and 5 buttons sent as OSC to any software (Chataigne, TouchDesigner, Max, QLab, Isadora…).

**[⬇️ Télécharger / Download](../../releases/latest)** — Windows · macOS (Apple Silicon / Intel) · Linux · Licence GPL v3

---

## 🇫🇷 Français

### Utilisation
1. Brancher le ShuttleXpress en USB et **fermer le logiciel Contour** s'il est installé.
2. Télécharger le zip de votre système dans [Releases](../../releases/latest), le décompresser.
3. Double-cliquer sur `ShuttleOSC` (`ShuttleOSC.exe` sous Windows) et **laisser la fenêtre ouverte**.
4. Dans votre logiciel, recevoir l'OSC sur le **port 9000**.

Premier lancement :
- **Windows** : « Windows a protégé votre ordinateur » → *Informations complémentaires* → *Exécuter quand même*.
- **macOS** : *Réglages Système* → *Confidentialité et sécurité* → *Ouvrir quand même*. Autoriser *Surveillance de l'entrée* si demandé.
- **Linux** : installer la règle udev (voir plus bas).

### Messages OSC
| Adresse | Valeur | Contrôle |
|---|---|---|
| `/shuttle/jog/up` | aucune | 1 message par cran vers la droite |
| `/shuttle/jog/down` | aucune | 1 message par cran vers la gauche |
| `/shuttle/ring` | -7 à 7 (0 = repos) | bague à ressort |
| `/shuttle/button/1` … `/5` | 1 appui, 0 relâchement | boutons |

### Options
```
ShuttleOSC --host 127.0.0.1 --port 9000 --debug
```
`--host` : ordinateur destinataire · `--port` : port OSC · `--debug` : affiche les données reçues et envoyées.

### Exemple avec ETC Eos (via Châtaigne)
| Shuttle | Message vers Eos |
|---|---|
| jog up / down | `/eos/wheel/fine/pan` ±1 |
| bague | `/eos/switch/tilt` (valeur de la bague, arrêt à 0) |
| boutons | `/eos/cues/fire`, `/eos/cues/stop`, `/eos/at/home`… |

### Depuis le code source
Avec [uv](https://docs.astral.sh/uv/) : `uv run shuttle_osc.py --debug` (Python et dépendances installés automatiquement).
Sans uv : Python 3.10 à 3.13, `pip install -r requirements.txt`, puis `python shuttle_osc.py`.

### Linux : règle udev
```
sudo cp 99-shuttlexpress.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```
Puis débrancher et rebrancher le Shuttle.

---

## 🇬🇧 English

### Usage
1. Plug in the ShuttleXpress and **quit the Contour software** if installed.
2. Download the zip for your system from [Releases](../../releases/latest) and unzip it.
3. Double-click `ShuttleOSC` (`ShuttleOSC.exe` on Windows) and **keep the window open**.
4. In your software, receive OSC on **port 9000**.

First launch:
- **Windows**: "Windows protected your PC" → *More info* → *Run anyway*.
- **macOS**: *System Settings* → *Privacy & Security* → *Open Anyway*. Allow *Input Monitoring* if asked.
- **Linux**: install the udev rule (see below).

### OSC messages
| Address | Value | Control |
|---|---|---|
| `/shuttle/jog/up` | none | 1 message per step clockwise |
| `/shuttle/jog/down` | none | 1 message per step counter-clockwise |
| `/shuttle/ring` | -7 to 7 (0 = rest) | spring-loaded ring |
| `/shuttle/button/1` … `/5` | 1 press, 0 release | buttons |

### Options
```
ShuttleOSC --host 127.0.0.1 --port 9000 --debug
```
`--host`: target computer · `--port`: OSC port · `--debug`: print incoming and outgoing data.

### Example with ETC Eos (through Chataigne)
| Shuttle | Message to Eos |
|---|---|
| jog up / down | `/eos/wheel/fine/pan` ±1 |
| ring | `/eos/switch/tilt` (ring value, stops at 0) |
| buttons | `/eos/cues/fire`, `/eos/cues/stop`, `/eos/at/home`… |

### From source
With [uv](https://docs.astral.sh/uv/): `uv run shuttle_osc.py --debug` (Python and dependencies installed automatically).
Without uv: Python 3.10 to 3.13, `pip install -r requirements.txt`, then `python shuttle_osc.py`.

### Linux: udev rule
```
sudo cp 99-shuttlexpress.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```
Then unplug and replug the Shuttle.

---

## 📜 Licence / License

🇫🇷 **GPL v3** : vous pouvez utiliser, modifier et redistribuer ce logiciel, mais toute version modifiée et distribuée doit rester open source sous la même licence. Voir [LICENSE](LICENSE).

🇬🇧 **GPL v3**: you may use, modify and redistribute this software, but any modified and distributed version must remain open source under the same license. See [LICENSE](LICENSE).

🇫🇷 Projet indépendant, non affilié à Contour Design ni à ETC. · 🇬🇧 Independent project, not affiliated with Contour Design or ETC.
