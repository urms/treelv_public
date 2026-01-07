# Installation und Verwendung des OpenStreetMap-Blocks

## Installation

### Schritt 1: Modul aktivieren

```bash
# Odoo neu starten mit dem neuen Modul
cd /Users/ulf/Develop/odoo
./start-odoo.sh
```

Oder das Modul über das Update-Skript installieren:

```bash
cd /Users/ulf/Develop/odoo
./update-module.sh -d <deine_datenbank> -m website_block_osm
```

### Schritt 2: Im Odoo-Backend installieren

1. Einloggen in Odoo
2. Zu **Apps** navigieren
3. Filter "Apps" entfernen (um alle Module zu sehen)
4. Nach "Website OpenStreetMap Block" suchen
5. Auf **Installieren** klicken

## Verwendung im Website-Builder

### 1. Block hinzufügen

1. Website-Editor öffnen (auf einer beliebigen Seite auf "Bearbeiten" klicken)
2. Auf **Blöcke** (links) klicken
3. Im Abschnitt nach dem OpenStreetMap-Block suchen
4. Den Block auf die gewünschte Position ziehen

### 2. Block konfigurieren

Nach dem Hinzufügen des Blocks erscheinen rechts die Optionen:

#### Adresse
- GPS-Koordinaten direkt eingeben, z.B. `(52.5200, 13.4050)` für Berlin
- Oder eine Adresse eingeben, die automatisch in Koordinaten umgewandelt wird

#### Marker-Stil
- **Standard**: Klassischer roter Leaflet-Marker
- **Benutzerdefiniert**: Dunkelblauer Custom-Marker

#### Karten-Stil
- **Standard**: Klassisches OpenStreetMap
- **Graustufen**: Schwarz-weiß für elegante Designs
- **Dunkel**: Dunkles Theme (gut für moderne Websites)
- **Wasserfarben**: Künstlerischer Look
- **Toner**: Minimalistisch, schwarz-weiß

#### Zoom
- Wert zwischen 1 (Weltkarte) und 18 (Straßenebene)
- Empfohlen: 12-15 für Stadtansichten

#### Beschreibung
- Optional: Fügt ein Textfeld am unteren Rand der Karte hinzu
- Kann angepasst werden (Text im HTML-Modus ändern)

## Vorteile gegenüber Google Maps

✅ **Keine API-Keys erforderlich**  
✅ **100% kostenlos** (bei normaler Nutzung)  
✅ **Datenschutzfreundlich** (kein Google-Tracking)  
✅ **Open Source**  
✅ **Mehrere Karten-Stile** verfügbar  

## Anpassungen

### Eigene Karten-Stile hinzufügen

Bearbeite [000.js](static/src/snippets/s_osm_map/000.js) und füge einen neuen Eintrag in `tileProviders` hinzu:

```javascript
myCustomStyle: {
    url: 'https://your-tile-server.com/{z}/{x}/{y}.png',
    attribution: 'Your attribution',
    maxZoom: 18,
}
```

Dann in [s_osm_map.xml](views/snippets/s_osm_map.xml) einen Button hinzufügen:

```xml
<we-button data-select-data-attribute="myCustomStyle">Mein Stil</we-button>
```

### Marker-Icon ändern

Ersetze [marker-icon-custom.svg](static/src/img/marker-icon-custom.svg) mit deinem eigenen SVG-Icon.

### Styling anpassen

Bearbeite [000.scss](static/src/snippets/s_osm_map/000.scss):

```scss
.s_osm_map {
    // Mindesthöhe ändern
    min-height: 200px;
    
    .description {
        // Beschreibungs-Overlay anpassen
        background: rgba(#000, 0.7);
    }
}
```

## Troubleshooting

### Karte wird nicht angezeigt

1. **Browser-Konsole prüfen**: F12 drücken und nach Fehlern suchen
2. **Leaflet geladen?**: Prüfe ob Leaflet-CSS und JS geladen wurden
3. **Assets neu generieren**: 
   ```bash
   odoo-bin -c config/odoo.conf -u website_block_osm --stop-after-init
   ```

### Marker erscheint nicht

1. Prüfe ob die GPS-Koordinaten korrekt sind (Format: `(lat,lng)`)
2. Stelle sicher, dass die Koordinaten im sichtbaren Bereich liegen

### Karte ist leer oder zeigt falschen Ort

1. Zoom-Level überprüfen (12-15 für Städte)
2. GPS-Koordinaten in korrektem Format: `(Breitengrad, Längengrad)`
3. Beispiel Berlin: `(52.5200, 13.4050)`

## Support & Weiterentwicklung

Für Fragen oder Feature-Requests:
- Code ansehen: `/Users/ulf/Develop/odoo/treelv_public/website_block_osm/`
- README: [README.md](README.md)

## Lizenz

LGPL-3 (wie Odoo)
