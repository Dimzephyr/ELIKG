"""Verify a downloaded paper-aligned release without changing its files."""
from pathlib import Path
import csv,json,sys,hashlib,math
from collections import Counter,defaultdict
import pyarrow.parquet as pq

def load(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def check(root):
    results={}
    for r in load(root/'manifest.csv'):
        p=root/r['file']
        assert p.stat().st_size==int(r['bytes']),r['file']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],r['file']
    results['manifest']='PASS'
    nodes=[json.loads(x) for x in (root/'knowledge_graph/nodes.jsonl').read_text(encoding='utf-8').splitlines()]
    edges=[json.loads(x) for x in (root/'knowledge_graph/relationships.jsonl').read_text(encoding='utf-8').splitlines()]
    ids={n['export_id'] for n in nodes}
    assert len(ids)==5036 and len(edges)==10342
    assert all(e['start_export_id'] in ids and e['end_export_id'] in ids for e in edges)
    active=Counter(e['properties'].get('active') for e in edges)
    assert active[True]==10295 and active[False]==47
    results['graph']={'nodes':len(ids),'relationships':len(edges),'active':active[True],'inactive':active[False]}
    cases=load(root/'evidence/review_cases_32.csv')
    assert len(cases)==32 and len({r['案例ID'] for r in cases})==32
    groups=Counter(r['适用性统计分组'] for r in cases)
    assert groups['目标未实质改变']==25 and groups['修订目标的条件支持']==2 and groups['原目标不适用']==5
    results['review_cases']=dict(groups)
    rows=load(root/'experiments/Table_main_selection_comparison.csv')
    assert len(rows)==7 and all(float(r['KBIS_lower_percent'])==0 for r in rows)
    assert sum(r['direction']=='POSITIVE' for r in rows)==5
    claims=load(root/'experiments/selected_claims_36.csv')
    assert len(claims)==36 and all(r['source_trace_status']=='PASS' for r in claims)
    assert len(load(root/'regional/configuration/main_text_configuration_24.csv'))==24
    assert len(load(root/'regional/references/regional_reference_constants_full.csv'))==122750
    results['selection_and_reference_counts']='PASS'
    pairs=pq.read_table(root/'regional/results/fixed_paired_objects.parquet').to_pylist()
    grouped=defaultdict(list)
    for r in pairs:grouped[r['ecosystem']].append(r)
    summary={r['ecosystem']:r for r in load(root/'regional/results/fixed_paired_summary.csv')}
    report={}
    for eco,group in grouped.items():
        weights=[float(r['estimator_weight']) for r in group];den=sum(weights)
        opposite=sum(w for r,w in zip(group,weights) if r['direction'] in {'KG_UP_VOR_DOWN','KG_DOWN_VOR_UP'})/den
        kg=sum(w*float(r['KG_delta']) for r,w in zip(group,weights))/den
        vor=sum(w*float(r['VOR_delta']) for r,w in zip(group,weights))/den
        expected=summary[eco]
        assert len(group)==int(expected['endpoint_objects'])
        assert math.isclose(opposite,float(expected['spatial_direction_disagreement_fraction']),abs_tol=2e-10),(eco,opposite,expected['spatial_direction_disagreement_fraction'])
        assert math.isclose(kg,float(expected['KG_delta']),abs_tol=2e-9),(eco,kg,expected['KG_delta'])
        assert math.isclose(vor,float(expected['VOR_delta']),abs_tol=2e-9),(eco,vor,expected['VOR_delta'])
        report[eco]={'objects':len(group),'opposite_fraction':opposite,'ELIKG_delta':kg,'Uniform_VOR_delta':vor}
    assert round(report['E4']['ELIKG_delta'],2)==1.65
    assert round(report['E4']['Uniform_VOR_delta'],2)==1.69
    assert round(report['E4']['opposite_fraction']*100,2)==39.12
    assert round(report['E7']['opposite_fraction']*100,2)==85.69
    results['paired_object_reaggregation']=report
    return results
if __name__=='__main__':
    print(json.dumps(check(Path(sys.argv[1])),ensure_ascii=False,indent=2))

