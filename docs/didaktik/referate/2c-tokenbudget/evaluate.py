"""Evaluate a saved, local study (Python stdlib). No model or network needed."""
import argparse, csv, hashlib, json, re, statistics as st
from collections import Counter
from pathlib import Path

def compact(x):
    return json.dumps(x, ensure_ascii=False, separators=(',', ':'))

def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()

def median_range(xs):
    return [round(f(xs),2) for f in (min,st.median,max)] if xs else None

def csvfile(path, rows):
    with path.open('w',newline='') as stream:
        w=csv.DictWriter(stream, fieldnames=rows[0],lineterminator="\n");w.writeheader();w.writerows(rows)

def read_json(p):
    return json.loads(p.read_text())

def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--runs',type=Path,help='Local completed output directory; omit to verify archived evidence')
    cli.add_argument('--out',type=Path,default=Path(__file__).parent/'evidence')
    args=cli.parse_args(); dest=args.out;dest.mkdir(parents=True,exist_ok=True); archive=dest/'records.jsonl'
    if args.runs:
        files=sorted(args.runs.glob('*.json'))
        records={p.name:read_json(p) for p in files}
        records['measured-bridge.ts']=(args.runs/'measured-bridge.ts').read_text()
        assert sha(records['measured-bridge.ts'])==records['environment.json']['sources']['apps/backend/src/lib/topic2c.experiment.test.ts']
        archive.write_text(''.join(compact({'file':f,'data':x})+'\n' for f,x in records.items()))
    else:
        source = archive if archive.is_file() else Path(__file__).parent / 'evidence/records.jsonl'
        records={r['file']:r['data'] for r in map(json.loads,source.read_text().splitlines())}
    rows=[]; ratings=[]; unique={}
    for r in sorted((x for f,x in records.items() if re.fullmatch(r'[PR]\d+-S\d+-[AB]\.json',f)),key=lambda x:x['stamp']):
        n,arm,rep=r['n'],r['arm'],r['rep']
        req=records[f'request-{n}-{arm}.json']
        assert sha(compact(req))==r['wireSha256'],r['id']
        fixture=records[f'fixture-{n}.json']
        assert sha(json.dumps(fixture,sort_keys=True,ensure_ascii=False,separators=(',',':')))==r['fixtureSha256']
        inp=records[f'context-{n}-A.json']['context']
        scope=inp['sources'] if arm=='A' else records[f'context-{n}-B.json']
        wire_ids={s['id'] for s in scope};full_ids={s['id'] for s in inp['sources']}
        raw=r.get('rawContent','')
        try: parsed=json.loads(raw); valid_json=True
        except ValueError: parsed={};valid_json=False
        bound=r.get('bound') or {}; elems=bound.get('statements',[])+bound.get('suggestedNextSteps',[])
        direct=sum(any(i.startswith('qa-question:') for i in s['sourceIds']) for s in elems)
        refs=[i for s in elems for i in s['sourceIds']]
        # Complete sourceIds strings visible even in an incomplete JSON document.
        rawrefs=[i for body in re.findall(r'"sourceIds"\s*:\s*\[([^\]]*)\]',raw) for i in re.findall(r'"([^"]+)"',body)]
        visible={'statements':bound.get('statements',[]),'steps':bound.get('suggestedNextSteps',[]),'limitations':bound.get('limitations',[])}
        digest=sha(compact(visible));unique[digest]=visible
        ut=r.get('usage') or {}; timer=r.get('timings') or {}; mode=(r.get('execution') or {}).get('effectiveMode')
        row=dict(id=r['id'],n=n,arm=arm,rep=rep,prompt=ut.get('prompt_tokens'),generated=ut.get('completion_tokens'),cached=timer.get('cache_n'),prefill_ms=timer.get('prompt_ms'),ttft_ms=r.get('ttftMs'),decode_ms=timer.get('predicted_ms'),http_ms=r.get('requestMs'),pack_ms=r['packMs'],component_ms=r['componentMs'],http=r.get('http'),finish=r.get('finish'),raw_json=valid_json,raw_sha=sha(raw),raw_complete_refs=len(rawrefs),raw_invalid_refs=sum(i not in wire_ids for i in rawrefs),mode=mode,fallback=((r.get('execution') or {}).get('fallback') or {}).get('reason'),bound_status=bound.get('status'),bound_refs=len(refs),bound_invalid=sum(i not in (wire_ids if mode=='full-context' else full_ids) for i in refs),direct_elements=direct,elements=len(elems),visible_sha=digest,cgroup_MiB=int(r.get('cgroupBytes',0))/2**20)
        rows.append(row)
        if rep:
            direct_score = 2 if elems and direct == len(elems) else int(bool(elems) and direct * 2 >= len(elems))
            ratings.append({'run': r['id'], 'visible_sha': digest, 'D1': direct_score})
    csvfile(dest/'runs.csv',rows)
    coding=read_json(Path(__file__).parent/'coding.json')
    provisional=[]
    for row in ratings:
        mark=coding.get(row['visible_sha'],{})
        dims={d:mark.get(d) for d in ('D2','D3','D4','D5')}
        total=row['D1']+sum(dims.values()) if None not in dims.values() else None
        provisional.append(dict(run=row['run'],visible_sha=row['visible_sha'],D1=row['D1'],**dims,total=total,reason=mark.get('reason','Neue Ausgabe: manuell bewerten')))
    csvfile(dest/'ratings.csv',provisional)
    (dest/'visible.json').write_text(json.dumps(unique,ensure_ascii=False,indent=2)+'\n')
    scored=[r for r in rows if r['rep']]
    assert len(scored)==20 and len(rows)==22 and len({r['id'] for r in rows})==22
    groups=[]; pairs=[]
    for n in (6,100):
        for arm in ('A','B'):
            g=[r for r in scored if r['n']==n and r['arm']==arm]
            assert len(g)==5
            stat={k:median_range([r[k] for r in g if r[k] is not None]) for k in ('prompt','generated','prefill_ms','ttft_ms','decode_ms','http_ms','component_ms','pack_ms','cgroup_MiB')}
            groups.append(dict(n=n,arm=arm,count=len(g),range_median=stat,ready_generative=sum(r['mode']=='full-context' and r['bound_status']=='ready' for r in g),modes=dict(Counter(r['mode'] for r in g)),reason=dict(Counter(str(r['fallback']) for r in g)),under90=sum(r['component_ms']<90000 for r in g),over8=sum(r['component_ms']>8000 for r in g),contentVariants=len({r['raw_sha'] for r in g})))
        for key in ('prefill_ms','ttft_ms','component_ms'):
            diffs=[]
            for rep in range(1,6):
                pair={r['arm']:r[key] for r in scored if r['n']==n and r['rep']==rep}
                if None not in pair.values(): diffs.append(pair['A']-pair['B'])
            pairs.append({'n':n,'metric':key,'A_minus_B_min_median_max_ms':median_range(diffs)})
    (dest/'summary.json').write_text(json.dumps({'groups':groups,'paired':pairs,'all_zero_cache':all(r['cached']==0 for r in rows),'visibleForms':len(unique),'rawForms':len({r['raw_sha'] for r in scored}),'raw_valid_json':sum(r['raw_json'] for r in scored),'fallbacks':sum(r['mode']=='extractive' for r in scored)},indent=2)+'\n')
    print(len(rows),'archived runs (2 pilot, 20 measured);',len(unique),'distinct bound contents')

if __name__=='__main__':
    main()
