# Evidence-Linked Indicator Knowledge Graph (ELIKG)

**Creator:** 王炳尧 (Bingyao Wang) · [ORCID 0009-0004-5708-3764](https://orcid.org/0009-0004-5708-3764)

Code and documentation for the Evidence-Linked Indicator Knowledge Graph (ELIKG) study subgraph, indicator selection experiments and regional assessment data.

## Scope

This repository provides graph-structure inspection/import, checks of deposited files, and reaggregation of the released comparison results. It includes the unchanged scientific functions of the study's KBIS baseline, without its private/full-text input bundle.

The accompanying published dataset contains the **ELIKG subgraph supporting the study: 5,036 nodes and 10,342 relationships, with a selected-property projection**, all 32 review outcomes, selection comparisons, regional configurations and exact references, annual/object-year scores, 89,302 paired objects, and sensitivity results.

The full research graph includes third-party text and semantic fields whose redistribution rights have not been verified; this release therefore provides the study subgraph and supporting data only. Third-party full text and restricted material are not redistributed. Original IDs, directions, states, retained numeric precision and all comparison outcomes are preserved. Data licence: CC BY 4.0 for author-owned contributions; code licence: MIT.

## Data availability

Data record: [Evidence-Linked Indicator Knowledge Graph (ELIKG): study subgraph, indicator selection experiments and regional assessment data (v1.0.0)](https://doi.org/10.5281/zenodo.23692391). DOI: **10.5281/zenodo.23692391**. Published on Zenodo. Archive file: `ELIKG_data.zip`; MD5: `244a504842dbfb9261487c072e567235`.

Extract the data directory as `ELIKG-data/`, or pass its actual location to the commands below. Data are deliberately not tracked in this code repository.

## Commands

```sh
python scripts/check_release.py /path/to/ELIKG-data
python scripts/rebuild_summary_tables.py /path/to/ELIKG-data
python scripts/import_graph.py /path/to/ELIKG-data
```

The first command verifies hashes, graph connectivity/states, case/task counts and paired results. The second reaggregates existing comparison results; neither runs new experiments or recalculates ecological scores. The third validates graph files and defaults to **dry-run**.

An optional write to a separate, empty local Neo4j database requires explicit `--write`, environment variables `ELIKG_NEO4J_URI`, `ELIKG_NEO4J_USER`, `ELIKG_NEO4J_PASSWORD`, and `--database`. Never point this example at the original research database.

`pyarrow` is required for typed Parquet checks. The Neo4j driver is needed only for the optional import. Exact original environment/model settings remain in the accompanying research data/metadata; these minimal requirements are for the release utilities, not a claim that the historic model service is reproducible indefinitely.

## Interpretation and provenance

- Preserve original fields: K0=KBIS; KPLUS/K+=EKRS.
- Original retrieval comparison: B=FER, C=GBR. Later optimized workflow comparison: B=EKRS, C=ELIKG. Do not apply one mapping across experiments.
- The workflow graph file had 8,363 relations; its recorded query policy quarantined one, giving 8,362 relations. The original FER/GBR input had 8,327. These inputs differ from the study subgraph released here.
- Review correction and reassessment concern the same 32 cases. Model sessions are not independent human-expert validation.
- Annual valid samples and fixed paired samples have different denominators. River direction shares use the released estimator weights. Historical similarity is not an independent ecological health threshold.
- Model-assisted extraction/selection/evaluation used gpt-6-astra/max. Codex assisted release preparation and checking. The creator takes responsibility for reviewing the materials.

See `docs/RELEASE_SCOPE.md` for exclusions and correspondence. Manuscript text, figures and research results have not been changed by this release.


