# Archived scientific functions; unchanged bodies from the study. Full frozen candidate/source input is not redistributed.
from pathlib import Path
import json,re,unicodedata,hashlib
D=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def normalize(s):return unicodedata.normalize('NFKC',s).casefold()
def terms(s):
 s=normalize(s);out=set(re.findall(r'[a-z0-9]+',s))
 for h in re.findall(r'[\u4e00-\u9fff]+',s):
  out.update(h[i:i+2] for i in range(len(h)-1))
  if len(h)==1:out.add(h)
 return sorted(out)
def text(f):
 # Values only: no IDs, reviewed outcome labels, old selection flags or scores.
 vals=[f['measurement_definition'],f['source_use'],f['researcher_mapping'].get('attribute','')]
 def strings(v):
  if isinstance(v,str):return [v]
  if isinstance(v,list):return [s for i in v for s in strings(i)]
  if isinstance(v,dict):return [s for k,i in v.items() if k not in ('identity','source_ids','source_cluster','text_access') for s in strings(i)]
  return []
 return normalize(' '.join(strings(vals)))
def definition_key(f):
 d={k:normalize(str(v)) for k,v in f['measurement_definition'].items() if k not in ('identity','aliases')}
 return json.dumps(d,ensure_ascii=False,sort_keys=True)
def select(task,facts):
 query=' '.join([task['ecosystem_name'],task['purpose']]+[a['attribute'] for a in task['core_attributes']])
 tt=terms(query);pool=[f for f in facts if task['ecosystem'] in f['researcher_mapping']['explicit_ecosystems']+f['researcher_mapping']['context_search_routes']]
 ranked=[]
 for f in pool:
  hits=[w for w in tt if w in text(f)]
  ranked.append({'fact_id':f['fact_id'],'matches':len(hits),'matched_terms':hits,'definition_key':definition_key(f)})
 ranked.sort(key=lambda r:(-r['matches'],r['fact_id']))
 seen=set();chosen=[]
 for r in ranked:
  r['duplicate_definition']=r['definition_key'] in seen
  seen.add(r['definition_key'])
  if r['matches']>0 and not r['duplicate_definition'] and len(chosen)<3:chosen.append(r['fact_id'])
 return {'task_id':task['task_id'],'query':query,'terms':tt,'pool_ids':sorted(f['fact_id'] for f in pool),'ranking':ranked,'selected':chosen}
