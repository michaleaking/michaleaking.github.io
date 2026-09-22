#!/usr/bin/env python3
"""
Convert an eBird "Download My Data" export into GeoJSON for the Fun map.

Two modes (set LIFE_BIRDS_ONLY below):
  * False -> EVERY sighting becomes a marker (default).
  * True  -> only the first sighting of each species (a classic life list).

Each feature gets a unique `id` = "<Submission ID>|<Common Name>". That id is
how you attach a photo to ONE specific sighting (see assets/data/bird_photos.json),
so a photo lands on the right date/place rather than on the first sighting.

Get the input file:
    eBird.org -> your account -> "Download My Data" -> Submit Request.
    Unzip the emailed file to find MyEBirdData.csv.

Usage:
    python scripts/ebird_to_geojson.py path/to/MyEBirdData.csv

Writes: assets/data/life_birds.geojson

Bird photos are NOT stored here — they live in assets/data/bird_photos.json,
keyed by sighting id, so re-running this script never overwrites them.

Requires: pandas
"""
import sys
import json
from pathlib import Path

import pandas as pd

LIFE_BIRDS_ONLY = False   # False = every sighting; True = first of each species
SPECIES_ONLY = True       # drop "gull sp.", hybrids, and slashes


def is_species(name: str) -> bool:
    name = str(name)
    if " sp." in name or "/" in name or "hybrid" in name.lower():
        return False
    return True


def main(csv_path: str) -> None:
    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Latitude", "Longitude", "Date", "Common Name"])
    if SPECIES_ONLY:
        df = df[df["Common Name"].map(is_species)]

    df = df.sort_values("Date")
    if LIFE_BIRDS_ONLY:
        df = df.groupby("Common Name", as_index=False).first()

    features = []
    for _, r in df.iterrows():
        sid = str(r.get("Submission ID", "") or "").strip()
        name = r["Common Name"]
        fid = f"{sid}|{name}" if sid else name
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point",
                         "coordinates": [float(r["Longitude"]), float(r["Latitude"])]},
            "properties": {
                "id": fid,
                "common_name": name,
                "scientific_name": r.get("Scientific Name", ""),
                "date": r["Date"].strftime("%Y-%m-%d"),
                "time": str(r.get("Time", "") or ""),
                "location": r.get("Location", ""),
                "count": str(r.get("Count", "") or ""),
                "checklist": f"https://ebird.org/checklist/{sid}" if sid else "",
            },
        })

    fc = {"type": "FeatureCollection", "features": features}
    out = Path(__file__).resolve().parents[1] / "assets" / "data" / "life_birds.geojson"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(fc, indent=1))
    mode = "life birds" if LIFE_BIRDS_ONLY else "sightings"
    print(f"Wrote {len(features)} {mode} to {out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python scripts/ebird_to_geojson.py path/to/MyEBirdData.csv")
    main(sys.argv[1])
