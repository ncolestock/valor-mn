#!/usr/bin/env python3
"""Rebuild feed.xml from podcast.json + episodes/*.json."""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITUNES = "http://www.itunes.com/dtds/podcast-1.0.dtd"
ATOM = "http://www.w3.org/2005/Atom"
CONTENT = "http://purl.org/rss/1.0/modules/content/"


def rfc2822(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return format_datetime(dt)


def duration_str(seconds: int) -> str:
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def main() -> None:
    cfg = json.loads((ROOT / "podcast.json").read_text())
    base = cfg["base_url"].rstrip("/")
    cover_url = f"{base}/{cfg['cover']}"

    episodes = []
    for p in sorted((ROOT / "episodes").glob("*.json"), reverse=True):
        ep = json.loads(p.read_text())
        audio = ROOT / "episodes" / ep["file"]
        if not audio.is_file():
            raise SystemExit(f"missing audio: {audio}")
        ep["_bytes"] = audio.stat().st_size
        ep["_audio_url"] = f"{base}/episodes/{ep['file']}"
        ep["_dt"] = datetime.fromisoformat(ep["date"])
        episodes.append(ep)

    ET.register_namespace("itunes", ITUNES)
    ET.register_namespace("atom", ATOM)
    ET.register_namespace("content", CONTENT)

    rss = ET.Element("rss", {"version": "2.0"})

    ch = ET.SubElement(rss, "channel")
    ET.SubElement(ch, "title").text = cfg["title"]
    ET.SubElement(ch, "link").text = cfg["link"]
    ET.SubElement(
        ch,
        f"{{{ATOM}}}link",
        {"href": f"{base}/feed.xml", "rel": "self", "type": "application/rss+xml"},
    )
    ET.SubElement(ch, "language").text = cfg["language"]
    ET.SubElement(ch, "copyright").text = cfg["copyright"]
    ET.SubElement(ch, "description").text = cfg["description"]
    ET.SubElement(ch, "lastBuildDate").text = rfc2822(datetime.now(timezone.utc))
    ET.SubElement(ch, "generator").text = "valor-mn/scripts/build_feed.py"
    ET.SubElement(ch, "docs").text = "https://help.apple.com/itc/podcasts_connect/#/itcb54353390"

    ET.SubElement(ch, f"{{{ITUNES}}}author").text = cfg["author"]
    ET.SubElement(ch, f"{{{ITUNES}}}summary").text = cfg["description"]
    ET.SubElement(ch, f"{{{ITUNES}}}type").text = cfg["type"]
    ET.SubElement(ch, f"{{{ITUNES}}}explicit").text = "true" if cfg["explicit"] else "false"
    ET.SubElement(ch, f"{{{ITUNES}}}image", {"href": cover_url})
    for cat in cfg["categories"]:
        el = ET.SubElement(ch, f"{{{ITUNES}}}category", {"text": cat["text"]})
        if cat.get("sub"):
            ET.SubElement(el, f"{{{ITUNES}}}category", {"text": cat["sub"]})
    owner = ET.SubElement(ch, f"{{{ITUNES}}}owner")
    ET.SubElement(owner, f"{{{ITUNES}}}name").text = cfg["owner_name"]
    ET.SubElement(owner, f"{{{ITUNES}}}email").text = cfg["email"]

    img = ET.SubElement(ch, "image")
    ET.SubElement(img, "url").text = cover_url
    ET.SubElement(img, "title").text = cfg["title"]
    ET.SubElement(img, "link").text = cfg["link"]

    for ep in episodes:
        item = ET.SubElement(ch, "item")
        ET.SubElement(item, "title").text = ep["title"]
        ET.SubElement(item, "description").text = ep["summary"]
        ET.SubElement(item, f"{{{ITUNES}}}summary").text = ep["summary"]
        ET.SubElement(item, f"{{{CONTENT}}}encoded").text = ep["summary"]
        ET.SubElement(item, "pubDate").text = rfc2822(ep["_dt"])
        ET.SubElement(item, "link").text = ep["_audio_url"]
        ET.SubElement(
            item,
            "enclosure",
            {
                "url": ep["_audio_url"],
                "length": str(ep["_bytes"]),
                "type": "audio/x-m4a",
            },
        )
        guid = ET.SubElement(item, "guid", {"isPermaLink": "false"})
        guid.text = ep["guid"]
        ET.SubElement(item, f"{{{ITUNES}}}duration").text = duration_str(ep["duration"])
        ET.SubElement(item, f"{{{ITUNES}}}explicit").text = (
            "true" if ep.get("explicit") else "false"
        )
        ET.SubElement(item, f"{{{ITUNES}}}episodeType").text = "full"

    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ")
    out = ROOT / "feed.xml"
    payload = ET.tostring(rss, encoding="unicode")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + payload + "\n"
    out.write_text(xml, encoding="utf-8")
    print(f"wrote {out} ({len(episodes)} episode(s))")


if __name__ == "__main__":
    main()
