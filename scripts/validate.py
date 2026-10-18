#!/usr/bin/env python3
"""Conservative static safeguards; does not replace testing on iPhone."""
from pathlib import Path
import ipaddress
ROOT = Path(__file__).resolve().parents[1]
source = (ROOT/"config/shadowrocket.conf").read_text(encoding="utf-8")
parts = {}
section = None
for line in source.splitlines():
    line = line.strip()
    if not line or line.startswith("#"): continue
    if line.startswith("[") and line.endswith("]"):
        section = line[1:-1]
        assert section not in parts, "duplicate section"
        parts[section] = []
    else:
        assert section, "content without section"
        parts[section].append(line)
assert set(parts)=={"General","Rule","MITM"}, "unexpected sections"
options = dict((x.split("=",1)[0].strip(),x.split("=",1)[1].strip()) for x in parts["General"] if "=" in x)
assert options["fallback-dns-server"]=="system"
assert options["dns-server"]=="https://dns.alidns.com/dns-query#no-h3,https://doh.pub/dns-query#no-h3"
assert parts["MITM"]==["enable = false"], "MITM forbidden"
rules=[]
for line in parts["Rule"]:
    items=[x.strip() for x in line.split(",")]
    if items[0]=="FINAL":
        assert len(items)==2 and items[1]=="PROXY"
        rules.append(("FINAL","",items[1]))
        continue
    assert len(items) in (3,4), "bad rule "+line
    typ, domain, policy = items[:3]
    assert typ in ("DOMAIN","DOMAIN-SUFFIX","IP-CIDR","GEOIP") and policy in ("DIRECT","PROXY","REJECT")
    if typ=="IP-CIDR": ipaddress.ip_network(domain)
    if len(items)==4: assert items[3]=="no-resolve"
    rules.append((typ,domain,policy))
assert rules[-1]==("FINAL","","PROXY") and sum(r[0]=="FINAL" for r in rules)==1
assert len({(r[0],r[1]) for r in rules})==len(rules),"duplicate matchers"
approved={x.strip() for x in (ROOT/"tests/approved_rejects.txt").read_text().splitlines() if x.strip() and not x.startswith("#")}
actual={",".join(r) for r in rules if r[2]=="REJECT"}
assert actual==approved, f"REJECT change requires review: {actual ^ approved}"
def route(host):
    for typ,domain,policy in rules:
        if typ=="DOMAIN" and host==domain: return policy
        if typ=="DOMAIN-SUFFIX" and (host==domain or host.endswith("."+domain)): return policy
        if typ=="FINAL": return policy
test={
 "music.apple.com":"DIRECT","appleid.apple.com":"DIRECT","buy.itunes.apple.com":"DIRECT",
 "miniapp.weixin.qq.com":"DIRECT","pay.weixin.qq.com":"DIRECT","wx.tenpay.com":"DIRECT",
 "api.alipay.com":"DIRECT","www.cmbchina.com":"DIRECT","api.meituan.com":"DIRECT",
 "chatgpt.com":"PROXY","api.openai.com":"PROXY","claude.ai":"PROXY",
 "gemini.google.com":"PROXY","api.spotify.com":"PROXY",
 "ads.spotify.com":"REJECT","adeventtracker.spotify.com":"REJECT"
}
for host,want in test.items(): assert route(host)==want,f"{host}: expected {want}, got {route(host)}"
print(f"PASS: {len(rules)} rules, {len(test)} static routing tests; no MITM, reviewed REJECT list.")
print("CAUTION: Static tests cannot verify real device, payments, DNS or Spotify audio ads.")
