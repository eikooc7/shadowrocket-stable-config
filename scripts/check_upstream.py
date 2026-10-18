#!/usr/bin/env python3
"""Weekly upstream check: candidates only, never update production automatically."""
from pathlib import Path
import urllib.request
ROOT = Path(__file__).resolve().parents[1]
URL="https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
watch={x.strip().lower() for x in (ROOT/"rules/review-watchlist.txt").read_text().splitlines()
       if x.strip() and not x.startswith("#")}
req=urllib.request.Request(URL, headers={"User-Agent":"stable-shadowrocket-check/1.0"})
with urllib.request.urlopen(req,timeout=25) as response:
    data=response.read(20000001)
if len(data)>20000000: raise SystemExit("upstream too large")
hosts=set()
for line in data.decode("utf-8",errors="replace").splitlines():
    bits=line.split("#",1)[0].split()
    if len(bits)>=2 and bits[0] in ("0.0.0.0","127.0.0.1"):
        hosts.update(h.lower() for h in bits[1:])
candidate=sorted(watch & hosts)
(ROOT/"rules/review-candidates.txt").write_text(
    "# Candidate domains from StevenBlack/hosts; NOT ACTIVE. Manual review required.\n"+
    "".join(h+"\n" for h in candidate), encoding="utf-8")
print(f"Checked {len(candidate)} inactive candidate domains")
