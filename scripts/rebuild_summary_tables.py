"""Reaggregate existing task results; no model calls or new ecological scoring."""
import csv,json,sys
from pathlib import Path
from collections import defaultdict

def load(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def summary(root):
    rows=load(root/'experiments/Table_main_selection_comparison.csv')
    fields=['KBIS_lower_percent','KBIS_upper_percent','ELIKG_lower_percent','ELIKG_upper_percent','ELIKG_minus_KBIS_lower_pp','ELIKG_minus_KBIS_upper_pp']
    by=defaultdict(list)
    for r in rows:by[r['task_id_frozen'].split('_')[0]].append(r)
    result={k:sum(sum(float(r[k]) for r in group)/len(group) for group in by.values())/len(by) for k in fields}
    return {'tasks':len(rows),'ecosystems':len(by),'confirmed_positive_tasks':sum(r['direction']=='POSITIVE' for r in rows),'four_ecosystem_equal_weight_percent_or_pp':result}
if __name__=='__main__':
    print(json.dumps(summary(Path(sys.argv[1])),ensure_ascii=False,indent=2))

