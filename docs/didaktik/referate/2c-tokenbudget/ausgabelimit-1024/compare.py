"""Check frozen inputs and compare matched 640/1024-token trials, offline."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from statistics import median


def load(path):
    return {r["file"]: r["data"] for r in map(json.loads, path.read_text().splitlines())}


def wire_hash(request):
    body = json.dumps(request, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()


def check_inputs(old, new):
    for name in old:
        if name.startswith(("fixture-", "context-")) or name in ("capacity.json", "controls.json"):
            assert old[name] == new[name], name
    original, replay = old["environment.json"], new["environment.json"]
    for key in ("release", "model", "serverSha", "quota", "cpu", "linux", "os", "node"):
        assert original[key] == replay[key], key
    for name, digest in original["sources"].items():
        if not name.endswith("/topic2c.experiment.test.ts"):
            assert replay["sources"][name] == digest, name
    for env in (original, replay):
        assert env["args"].count("--n-predict") == 1
    args = original["args"].copy()
    pos = args.index("--n-predict") + 1
    assert args[pos] == "640"
    args[pos] = "1024"
    assert args == replay["args"]
    expected = {f"R{rep}-S{n}-{arm}.json" for rep in range(1, 6) for n in (6, 100) for arm in "AB"}
    expected.update(("P0-S100-A.json", "P0-S100-B.json"))
    for archive in (old, new):
        assert {k for k in archive if re.fullmatch(r"[PR]\d+-S\d+-[AB]\.json", k)} == expected
    order = sorted(expected, key=lambda k: old[k]["stamp"])
    assert order == sorted(expected, key=lambda k: new[k]["stamp"])
    for name in order:
        first, second = old[name], new[name]
        req = f"request-{first['n']}-{first['arm']}.json"
        assert old[req]["max_tokens"] == 640 and new[req] == {**old[req], "max_tokens": 1024}, req
        for record, request in ((first, old[req]), (second, new[req])):
            assert record["wireSha256"] == wire_hash(request) and record["kvErased"], name
            assert record["usage"]["prompt_tokens_details"]["cached_tokens"] == 0, name
        assert first["fixtureSha256"] == second["fixtureSha256"], name
        assert first["usage"]["prompt_tokens"] == second["usage"]["prompt_tokens"], name
    return [name for name in order if name.startswith("R")]


def paired(first, second, request):
    context = json.loads(request["messages"][2]["content"])
    sources = context["sources"] if first["arm"] == "A" else context
    allowed = {s["id"] for s in sources}
    row = {"id": first["id"], "n": first["n"], "arm": first["arm"]}
    for cap, r in ((640, first), (1024, second)):
        try:
            raw = json.loads(r["rawContent"])
            row[f"json_{cap}"] = True
        except ValueError:
            raw = None
            row[f"json_{cap}"] = False
        # Only a schema-accepted generator response has auditable statement lists.
        row[f"unknown_source_refs_{cap}"] = None
        if r["execution"]["effectiveMode"] == "full-context":
            output = raw["output"]
            items = output["statements"] + output["suggestedNextSteps"]
            row[f"unknown_source_refs_{cap}"] = sum(
                source not in allowed for item in items for source in item["sourceIds"]
            )
        row[f"tokens_{cap}"] = r["usage"]["completion_tokens"]
        row[f"finish_{cap}"] = r["finish"]
        row[f"mode_{cap}"] = r["execution"]["effectiveMode"]
        row[f"status_{cap}"] = r["bound"]["status"]
        for metric, value in (("component", r["componentMs"]), ("http", r["requestMs"]),
                              ("ttft", r["ttftMs"]), ("decode", r["timings"]["predicted_ms"])):
            row[f"{metric}_{cap}_ms"] = round(value, 3)
    for metric in ("component", "http", "ttft", "decode"):
        row[f"{metric}_delta_ms"] = round(row[f"{metric}_1024_ms"] - row[f"{metric}_640_ms"], 3)
    row["component_delta_pct"] = round(100 * row["component_delta_ms"] / row["component_640_ms"], 3)
    row["identical_raw_prefix"] = second["rawContent"].startswith(first["rawContent"])
    return row


def main():
    here = Path(__file__).resolve().parent
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--archive", type=Path, default=here / "records.jsonl")
    cli.add_argument("--pairs", type=Path, help="Write CSV with all 20 scored pairs")
    args = cli.parse_args()
    old, new = load(here.parent / "evidence/records.jsonl"), load(args.archive)
    rows = []
    for k in check_inputs(old, new):
        run = new[k]
        rows.append(paired(old[k], run, new[f"request-{run['n']}-{run['arm']}.json"]))
    if args.pairs:
        with args.pairs.open("w", newline="") as target:
            writer = csv.DictWriter(target, fieldnames=rows[0], lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    for n, arm in ((6, "A"), (6, "B"), (100, "A"), (100, "B"), (None, None)):
        group = [r for r in rows if not n or (r["n"], r["arm"]) == (n, arm)]
        stats = {key: round(median(r[key] for r in group), 3) for key in (
            "component_640_ms", "component_1024_ms", "component_delta_ms", "component_delta_pct",
            "decode_delta_ms", "ttft_delta_ms")}
        print(n or "alle", arm or "", stats,
              "JSON", sum(r["json_1024"] for r in group),
              "generativ/ready", sum(r["mode_1024"] == "full-context" and r["status_1024"] == "ready" for r in group))


if __name__ == "__main__":
    main()
