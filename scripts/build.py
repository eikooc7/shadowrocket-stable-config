#!/usr/bin/env python3
"""Build immutable validated static artifact for GitHub Pages."""
import hashlib, json, shutil
from pathlib import Path
from datetime import datetime, timezone
from validate import ROOT
import validate
# validate.py enforces invariants during import
src = ROOT/"config/shadowrocket.conf"
out = ROOT/"site"
out.mkdir(exist_ok=True)
shutil.copyfile(src,out/"shadowrocket.conf")
(out/"version.json").write_text(json.dumps({
 "sha256":hashlib.sha256(src.read_bytes()).hexdigest(),
 "built_at_utc":datetime.now(timezone.utc).isoformat()
},indent=2)+"\n",encoding="utf-8")
(out/"index.html").write_text("""<!doctype html><html lang="zh"><meta charset="utf-8"><title>Shadowrocket Stable</title><body><h1>Shadowrocket Stable</h1><p><a href="./shadowrocket.conf">订阅配置</a></p><p><a href="./version.json">Version hash</a></p></body></html>""",encoding="utf-8")
print("Built site/shadowrocket.conf")
