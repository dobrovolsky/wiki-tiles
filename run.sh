#!/bin/bash

LANGS=("ca" "cs" "en" "es" "eu" "de" "fr" "it" "nl" "pt-BR" "tr" "zh" "uk" "ru")

if [ ! -f "latest-all.json.bz2" ]; then
    wget https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2
fi

rm -rf geojson
mkdir geojson
_pv() { command -v pv &>/dev/null && pv --force || cat; }
lbzip2 -dc latest-all.json.bz2 | _pv | grep '"P625"' | uv run app.py ${LANGS[@]}

rm -rf tiles
mkdir tiles
for lang in "${LANGS[@]}"; do
    uv tool run tippecanoe \
        -o "tiles/${lang}.mbtiles" \
        --layer=wiki \
        --minimum-zoom=7 \
        --maximum-zoom=14 \
        --drop-rate=1.4 \
        --no-feature-limit \
        --no-tile-size-limit \
        -L "wiki:geojson/${lang}.geojsonl"
done

rm -rf pbf
mkdir pbf
for lang in "${LANGS[@]}"; do
    uv tool run --from mbutil mb-util tiles/${lang}.mbtiles "pbf/${lang}_tiles" --image_format=pbf
done