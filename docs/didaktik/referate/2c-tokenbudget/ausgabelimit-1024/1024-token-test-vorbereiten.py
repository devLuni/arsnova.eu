"""Prepare an isolated replay from the four archived 640-token wire requests."""
import argparse
import hashlib
import json
from pathlib import Path
from shutil import copyfile

study = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("destination", type=Path, help="New directory under the repository's tmp/")
dest = parser.parse_args().destination
for line in (study / "messdaten-640/SHA256SUMS").read_text().splitlines():
    checksum, name = line.split(maxsplit=1)
    if hashlib.sha256((study / name).read_bytes()).hexdigest() != checksum:
        raise ValueError(f"Changed baseline artifact: {name}")
records = {
    row["file"]: row["data"]
    for row in map(json.loads, (study / "messdaten-640/messarchiv.jsonl").read_text().splitlines())
}
payloads = {}
for size in (6, 100):
    for arm in ("A", "B"):
        key = f"{size}-{arm}"
        request = records[f"request-{key}.json"]
        if request["max_tokens"] != 640:
            raise ValueError(f"Unexpected baseline limit for {key}")
        payloads[key] = {**request, "max_tokens": 1024}

# Reuse the exact measured harness, including timers, order, adapter and source binder.
bridge = records["measured-bridge.ts"]
start = bridge.index("      const b=JSON.parse(input.body!)")
end = bridge.index("      rec.wireSha256=", start)
bridge = bridge[:start] + "      const b=frozen[n+'-'+arm];\n" + bridge[end:]
declarations = "const trials:any[]=[];"
if bridge.count(declarations) != 1:
    raise ValueError("Cannot locate the declarations in the archived bridge")
frozen = json.dumps(payloads, ensure_ascii=False, separators=(",", ":"))
bridge = bridge.replace(declarations, f"const frozen:Record<string,any>={frozen};\n{declarations}")
startup = (study / "qwen-testserver.py").read_text()
limit = "'--n-predict','640'"
if startup.count(limit) != 1:
    raise ValueError("Cannot identify the original server ceiling")

dest.mkdir(parents=True, exist_ok=False)
(dest / "qa-kurzfassung-tokenbudget.test.ts").write_text(bridge)
(dest / "qwen-testserver.py").write_text(startup.replace(limit, "'--n-predict','1024'"))
copyfile(study / "qa-tests-ausfuehren.sh", dest / "qa-tests-ausfuehren.sh")
