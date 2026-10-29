#!/usr/bin/env python3
"""Regenerate assets/stats.svg from live GitHub data (public contributions only)."""
import json
import os
import re
import urllib.request

USER = "Rachit-Sharma08"
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "stats.svg")


def api(url, payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": "Bearer " + TOKEN,
            "Accept": "application/vnd.github+json",
            "User-Agent": "stats-refresh",
        },
    )
    return json.load(urllib.request.urlopen(req, timeout=30))


def main():
    # Unauthenticated public profile view: exactly the public-only number
    # visitors see (GitHub hides private contributions from other viewers).
    req = urllib.request.Request(
        "https://github.com/users/%s/contributions" % USER,
        headers={"User-Agent": "Mozilla/5.0 (compatible; stats-refresh)"},
    )
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    m = re.search(r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year", html, re.I)
    if not m:
        raise SystemExit("contribution total not found in public profile")
    contrib = int(m.group(1).replace(",", ""))
    u = api("https://api.github.com/users/" + USER)
    repos, followers = u["public_repos"], u["followers"]

    # Count-up: 8 quick frames then the final value, plays once per page load.
    texts = []
    for i in range(8):
        v = round(contrib * i / 8)
        s = round(i / 10, 3)
        e = round((i + 1) / 10, 3)
        texts.append(
            '<text x="128" y="82" font-size="32" font-weight="700" fill="#ffffff" opacity="0">%d'
            '<animate attributeName="opacity" dur="1s" values="0;0;1;1;0;0" '
            'keyTimes="0;%s;%s;%s;%s;1"/></text>' % (v, s, s, e, round(e + 0.005, 3))
        )
    texts.append(
        '<text x="128" y="82" font-size="32" font-weight="700" fill="#ffffff">%d+'
        '<animate attributeName="opacity" dur="1s" values="0;0;1" keyTimes="0;0.8;1"/></text>'
        % contrib
    )

    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 120" width="720" height="120" role="img" aria-label="GitHub stats: %d plus contributions in the last year from public repositories, %d public repositories, %d followers">
  <rect width="720" height="120" rx="14" fill="#1c0d13" stroke="#d62e4a" stroke-opacity="0.35"/>
  <rect x="14" y="0" width="0" height="4" rx="2" fill="#e8455f">
    <animate attributeName="width" dur="0.9s" from="0" to="692" fill="freeze"/>
  </rect>
  <text x="28" y="36" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="700" fill="#e8455f">GITHUB STATS</text>
  <line x1="238" y1="52" x2="238" y2="100" stroke="#d62e4a" stroke-opacity="0.25"/>
  <line x1="458" y1="52" x2="458" y2="100" stroke="#d62e4a" stroke-opacity="0.25"/>
  <g font-family="Arial, Helvetica, sans-serif" text-anchor="middle">
    %s
    <text x="128" y="104" font-size="13" fill="#e8455f">public contributions</text>
    <text x="348" y="82" font-size="32" font-weight="700" fill="#ffffff">%d</text>
    <text x="348" y="104" font-size="13" fill="#e8455f">public repos</text>
    <text x="568" y="82" font-size="32" font-weight="700" fill="#ffffff">%d</text>
    <text x="568" y="104" font-size="13" fill="#e8455f">followers</text>
  </g>
</svg>
''' % (contrib, repos, followers, "\n    ".join(texts), repos, followers)

    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print("stats.svg: contributions=%d public_repos=%d followers=%d" % (contrib, repos, followers))


if __name__ == "__main__":
    main()
