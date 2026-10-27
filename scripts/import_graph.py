"""Validate by default; optional import into a separate empty local Neo4j database."""
import argparse,json,os,re
from pathlib import Path
def main():
    p=argparse.ArgumentParser()
    p.add_argument('data',type=Path)
    p.add_argument('--write',action='store_true')
    p.add_argument('--database',default='elikg-public')
    a=p.parse_args()
    nodes=[json.loads(x) for x in (a.data/'knowledge_graph/nodes.jsonl').read_text(encoding='utf-8').splitlines()]
    edges=[json.loads(x) for x in (a.data/'knowledge_graph/relationships.jsonl').read_text(encoding='utf-8').splitlines()]
    ids={n['export_id'] for n in nodes}
    assert len(ids)==5036 and len(edges)==10342
    assert all(e['start_export_id'] in ids and e['end_export_id'] in ids for e in edges)
    if not a.write:
        print(json.dumps({'mode':'dry-run','nodes':len(ids),'relationships':len(edges),'writes':0}));return
    uri=os.environ['ELIKG_NEO4J_URI']
    if not uri.startswith(('bolt://localhost','bolt://127.0.0.1','neo4j://localhost','neo4j://127.0.0.1')):raise ValueError('This example only imports into a local separate database')
    from neo4j import GraphDatabase
    with GraphDatabase.driver(uri,auth=(os.environ['ELIKG_NEO4J_USER'],os.environ['ELIKG_NEO4J_PASSWORD'])) as driver:
        with driver.session(database=a.database) as s:
            assert s.run('MATCH (n) RETURN count(n) AS n').single()['n']==0,'Use a separate EMPTY database'
            for n in nodes:
                labels=n['labels']
                if not all(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',label) for label in labels):raise ValueError('Unexpected node label')
                label_clause=''.join(':'+label for label in labels if label!='ELIKGPublicNode')
                s.run('CREATE (n:ELIKGPublicNode'+label_clause+') SET n=$props, n.release_export_id=$id',props=n['properties'],id=str(n['export_id'])).consume()
            for e in edges:
                typ=e['type']
                if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',typ):raise ValueError('Unexpected relationship type')
                s.run('MATCH (a:ELIKGPublicNode {release_export_id:$a}), (b:ELIKGPublicNode {release_export_id:$b}) CREATE (a)-[r:'+typ+']->(b) SET r=$props',a=str(e['start_export_id']),b=str(e['end_export_id']),props=e['properties']).consume()
    print('Imported public metadata projection only; not the full-property research database.')
if __name__=='__main__':main()

