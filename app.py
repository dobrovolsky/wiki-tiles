"""
uv run app.py en uk
"""

import sys
import orjson

LANGS = tuple(sys.argv[1:]) or ("en",)

WIKI_LANG_OVERRIDES = {
    "pt-BR": "pt",
    "zh-HK": "zh",
}


def wiki_lang(lang: str) -> str:
    return WIKI_LANG_OVERRIDES.get(lang, lang)


def cleanup(line: bytes) -> bytes:
    return line.rstrip(b",\n").rstrip(b"\n")


def label_value(article: dict, lang: str) -> str | None:
    labels = article.get("labels", {})
    candidates = (lang, wiki_lang(lang), lang.split("-")[0])

    for candidate in candidates:
        label = labels.get(candidate)
        if label and label.get("value"):
            return label["value"]

    return None


def process_row(line: bytes, outputs: dict):
    line = cleanup(line)
    if not line or line in (b"[", b"]"):
        return

    try:
        article = orjson.loads(line)
    except Exception:
        return

    if article.get("type") != "item":
        return

    p625 = article.get("claims", {}).get("P625", [])
    if not p625:
        return
    try:
        location = p625[0]["mainsnak"]["datavalue"]["value"]
        lat, lon = location["latitude"], location["longitude"]
    except KeyError, IndexError:
        return

    sitelinks = article.get("sitelinks", {})

    for lang in LANGS:
        sitelink = sitelinks.get(f"{wiki_lang(lang)}wiki")
        if not sitelink:
            continue

        article_title = sitelink["title"]

        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "wiki_id": article["id"],
                "label": label_value(article, lang) or article_title,
                "wiki_title": article_title,
            },
        }

        outputs[lang].write(orjson.dumps(feature))
        outputs[lang].write(b"\n")


def main():
    import os

    os.makedirs("geojson", exist_ok=True)
    outputs = {lang: open(f"geojson/{lang}.geojsonl", "wb") for lang in LANGS}

    try:
        for line in sys.stdin.buffer:
            process_row(line, outputs)
    finally:
        for f in outputs.values():
            f.close()


if __name__ == "__main__":
    main()
