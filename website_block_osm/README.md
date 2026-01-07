# Website OpenStreetMap Block

Dieses Odoo-Modul fügt einen OpenStreetMap/Leaflet-Block zur Website hinzu, als Alternative zum Google Maps Block.

## Features

- 🗺️ **OpenStreetMap-Integration** mit Leaflet
- 🎨 **Mehrere Karten-Stile**: Standard, Graustufen, Dunkel, Wasserfarben, Toner
- 📍 **GPS-Positionsauswahl** über den Website-Editor
- 🔍 **Zoom-Kontrolle** (1-18)
- 📌 **Anpassbare Marker**: Standard oder benutzerdefiniert
- 💬 **Optionale Beschreibung** als Overlay

## Installation

1. Modul in den Odoo-Addons-Pfad kopieren (z.B. `treelv_public/website_block_osm/`)
2. Odoo neu starten oder Apps-Liste aktualisieren
3. Im Odoo-Backend zu Apps gehen
4. Nach "Website OpenStreetMap Block" suchen
5. Installieren klicken

## Verwendung

1. Website-Editor öffnen
2. Auf "Blöcke" klicken
3. Im Abschnitt "Dynamischer Inhalt" das OpenStreetMap-Element finden
4. Auf die Seite ziehen
5. Block anklicken und rechts im Editor folgende Optionen anpassen:
   - **Adresse**: GPS-Koordinaten oder Adresse eingeben
   - **Marker-Stil**: Standard oder benutzerdefiniert
   - **Karten-Stil**: Verschiedene Designs wählen
   - **Zoom**: Zoom-Level einstellen (1-18)
   - **Beschreibung**: Optionales Text-Overlay ein-/ausschalten

## Verfügbare Karten-Stile

- **Standard**: Klassisches OpenStreetMap-Design
- **Graustufen**: Schwarz-weiße Karte
- **Dunkel**: Dunkles Theme für moderne Websites
- **Wasserfarben**: Künstlerischer Aquarell-Look
- **Toner**: Minimalistisches schwarz-weißes Design

## Technische Details

- **Leaflet Version**: 1.9.4
- **Tile-Provider**: OpenStreetMap, CartoDB, Stadia Maps
- **JavaScript**: Odoo publicWidget
- **SCSS**: Bootstrap-kompatible Styles

## Abhängigkeiten

- `website` (Odoo Core-Modul)
- Leaflet (wird automatisch von CDN geladen)

## Lizenz

LGPL-3

## Autor

Basierend auf dem Original Google Maps Block von Odoo, angepasst für OpenStreetMap/Leaflet.

## Hinweise

- Keine API-Keys erforderlich (im Gegensatz zu Google Maps)
- 100% Open Source
- Datenschutzfreundlich (keine Tracking-Cookies von Google)
