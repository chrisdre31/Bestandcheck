#!/bin/sh
# Baut die App neu aus dem aktuellen Excel-Export.
# Aufruf (im Repository):  sh quelle/aktualisieren.sh /pfad/zu/app_daten.json
set -e
cd "$(dirname "$0")"
python3 build_data.py "$1" appdata.json
python3 make_site.py ..
