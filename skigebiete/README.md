# Pulverbericht

Web-App für Schweizer Lieblingsskigebiete: Schneehöhen, 7-Tage-Wetter und das aktuelle SLF-Lawinenbulletin mit gefährdeten Expositionen und Höhenlagen.

## Datenquellen
| Was | Quelle | Abruf |
|---|---|---|
| Lawinenbulletin (Gefahrenstufe, Lawinenprobleme, Expositionen, Höhen) | SLF, `aws.slf.ch/api/bulletin/caaml/de/geojson` | direkt im Browser |
| Gemessene Schneehöhe | SLF IMIS-Messnetz, `measurement-api.slf.ch` | stündlich per GitHub Action → `data/imis.json` (die API erlaubt keinen Browserzugriff) |
| Wetter, modellierte Schneehöhe Berg/Tal | Open-Meteo | direkt im Browser |

## Starten
Lokal: `cd skigebiete && python3 -m http.server` → http://localhost:8000

Online: GitHub Pages für das Repo aktivieren, dann unter `…/skigebiete/` aufrufen.

Die Action `.github/workflows/schnee-daten.yml` läuft nur auf dem Default-Branch (`main`). Fehlt `data/imis.json` lokal, lädt die App die Datei von `main` auf GitHub.

Lieblingsgebiete (25 vorgegebene + eigene mit Koordinaten) werden im Browser gespeichert.
