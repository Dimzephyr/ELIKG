# Release scope and correspondence

This release uses the archived study sources identified by the source checksums in the data manifest.

| Manuscript content | Supporting release |
| --- | --- |
| Fig. 2–3: actual graph evidence examples | knowledge_graph/ plus evidence/; original IDs, relation direction and active state retained |
| Review outcomes | evidence/review_cases_32.csv and review_stage_counts.csv |
| Fig. 4 and selection comparisons | experiments/: KBIS, EKRS, ELIKG, FER/GBR; unsuccessful/unfinished and budget records retained |
| Table 2 regional configurations | regional/configuration/ |
| Fig. 5 and annual changes | regional/results/regional_year_series.csv, object_year_scores.parquet and component tables |
| Fig. 6 and paired direction shares | fixed_paired_objects.parquet, fixed_paired_summary.csv and paired_year_series.csv |
| Supplementary sensitivity/diagnostics | weights, D90/D95/D99, LOYO and observation-result tables |
| Scoring definitions | regional/references/ and configuration fields |

## What is omitted

- Third-party full text, long source excerpts and unreviewed nested text properties.
- Full main research graph and native database dump.
- Raw satellite products and geospatial geometry/base maps whose redistribution has not been cleared.
- Private communication or credentials.
- Source-text input needed for an exact replay of historical retrieval/model sessions.

A graph property projection is not a full-property database. All original nodes and directed relationships of the selected repaired snapshot remain; omitted property names are listed per entity. No synthetic replacement edges or new scientific attributes are added. The public projection cannot be used to claim access to every original evidence passage.

The release enables numerical inspection/reaggregation of deposited outcomes and graph structure inspection, not full map geometry reconstruction or end-to-end source retrieval. Named source papers/products remain accessible through their original providers and licences.

The 221,053/498,216 main-graph counts describe the study archive, not the size of this compact public graph. Source text and machine candidate graphs are distinct from verified application cases. This distinction is part of the release, not a change to the manuscript's observations.


