#!/usr/bin/env python3
"""Refresh data/metrics.json from Google Scholar (primary) or OpenAlex ORCID (fallback)."""

import datetime
import json
import pathlib
import urllib.request

METRICS_PATH = pathlib.Path(__file__).resolve().parent.parent / "data" / "metrics.json"
SCHOLAR_ID = "4TMRXlUAAAAJ"
ORCID_ID = "0009-0009-1897-5811"


def fetch_google_scholar():
    from scholarly import scholarly
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["basics", "indices"])
    citedby = author.get("citedby")
    hindex = author.get("hindex")
    i10index = author.get("i10index")
    if citedby is None:
        raise RuntimeError("Missing citation count from Google Scholar")
    return {
        "citations": int(citedby),
        "h_index": int(hindex or 0),
        "i10_index": int(i10index or 0),
        "source": "Google Scholar",
    }


def fetch_openalex():
    url = f"https://api.openalex.org/authors/orcid:{ORCID_ID}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Lewis-Hou.github.io (mailto:zhangshuai@nju.edu.cn)"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return {
        "citations": int(data.get("cited_by_count", 0)),
        "h_index": int(data.get("summary_stats", {}).get("h_index", 0)),
        "i10_index": int(data.get("summary_stats", {}).get("i10_index", 0)),
        "source": "OpenAlex",
    }


def main():
    current = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    updated = None
    try:
        updated = fetch_google_scholar()
        print("Fetched Google Scholar metrics:", updated)
    except Exception as exc:
        print(f"Google Scholar fetch skipped ({exc}); falling back to OpenAlex...")
        try:
            updated = fetch_openalex()
            print("Fetched OpenAlex metrics:", updated)
        except Exception as exc2:
            print(f"OpenAlex fetch failed ({exc2}); keeping existing metrics.")
            return

    if updated and updated["citations"] >= current.get("citations", 0) * 0.5:
        current.update(updated)
        current["updated_at"] = datetime.date.today().isoformat()
        METRICS_PATH.write_text(
            json.dumps(current, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print("Updated", METRICS_PATH)


if __name__ == "__main__":
    main()
