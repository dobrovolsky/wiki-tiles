# Wiki tiles

Generate vector tiles with wikipedia articles.

## Run

You can use dockes as well or install reqired tools and do it on your
machine. Required tools: `uv`, `lbzip2`. Optional: `pv` (progress display).

```bash
podman build -t wiki-tiles .

podman run --rm \
    -v "$(pwd):/app" \
    -v "uv-cache:/root/.cache/uv" \
    wiki-tiles bash run.sh
```

## Flow

For actual details see: `run.sh`

But it works in this way:

- Downloads json dump from [wikimedia](https://dumps.wikimedia.org/)
- Extract articles that has `P625` (geolocation)
- Transform into GeoJSONL file (regular [jsonl](https://jsonlines.org/))
- [Tippecanoe](https://github.com/felt/tippecanoe) generates `mbtiles`
- [mbutil](https://github.com/mapbox/mbutil) converts into regular `z/x/y.pbf`

## Testing

For testing porposes you don't need all dump you can download part file.
Or process it without downlaoding file on disc.

```bash
curl -L -r 0-1000000 https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2 | lbzip2 -dc | grep '"P625"'
```

Notice: you always should start from 0.