#!/usr/bin/env python3
"""Holt die aktuellen Schneehöhen aller IMIS-Messstationen des SLF und
schreibt eine kompakte JSON-Datei für die Skigebiets-App.

Die SLF-Mess-API sendet keine CORS-Header, daher kann der Browser sie nicht
direkt abfragen. Dieses Skript läuft stündlich per GitHub Action.
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://measurement-api.slf.ch/public/api/imis"
OUT = Path(__file__).resolve().parent.parent / "data" / "imis.json"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "skigebiete-app/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def main():
    stations = get(f"{BASE}/stations")
    measurements = get(f"{BASE}/measurements")  # letzte 24 h, alle Stationen

    series = {}
    for m in measurements:
        if m.get("HS") is None:
            continue
        series.setdefault(m["station_code"], []).append(m)

    out = []
    for st in stations:
        rows = sorted(series.get(st["code"], []), key=lambda m: m["measure_date"])
        if not rows:
            continue
        last, first = rows[-1], rows[0]
        hours = (parse_ts(last["measure_date"]) - parse_ts(first["measure_date"])).total_seconds() / 3600
        out.append({
            "code": st["code"],
            "name": st["label"],
            "lat": round(st["lat"], 5),
            "lon": round(st["lon"], 5),
            "elev": round(st["elevation"]),
            "canton": st.get("canton_code"),
            "hs": round(last["HS"]),
            "hs24": round(last["HS"] - first["HS"]) if hours >= 20 else None,
            "ta": last.get("TA_30MIN_MEAN"),
            "time": last["measure_date"],
        })

    if not out:
        sys.exit("Keine Messwerte erhalten – Datei bleibt unverändert.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "source": "WSL-Institut für Schnee- und Lawinenforschung SLF, IMIS-Messnetz",
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stations": sorted(out, key=lambda s: s["code"]),
    }, ensure_ascii=False, separators=(",", ":")))
    print(f"{len(out)} Stationen geschrieben → {OUT}")


if __name__ == "__main__":
    main()
