# Coherence metrics for benchmarked systems — BioML 2026 (Task 1, global alignment)

**Short answer: yes, we calculated them.** They were *not* in `REPAIR_OUTPUTS` (that
tree holds reference-alignment repair experiments only). They live on `xgpu` at:

```
/home/jon/bioml_workspace/bioml_repos/OAEI-Bio-ML-private/results/coherence/
  <SYSTEM>__coherence_global_<PAIR>_scores__<ELK|HermiT>.json
```

Byte-identical duplicates also sit at the root of that repo.

## What was measured

Per `COHERENCE_PROCEDURE.md` and the driver scripts (`aml_compute_coherence.sh`,
`logmap_compute_coherence.sh`, `logmap_lt_compute_coherence.sh`,
`bertmap_compute_coherence.sh`, `bertmap_lt_compute_coherence.sh`,
`lexical_compute_coherence.sh`, `ref_compute_coherence.sh`):

each **matcher's own output** (`.../release/private/baselines/<matcher>/<PAIR>/global.rdf`)
is merged with both source OWLs — one `EquivalentClasses(src, tgt)` per `=`
correspondence — classified, and then:

- `unsatisfiable_count` — unsatisfiable named classes in the merged ontology
- `union_class_count` — merged named-class signature (the denominator)
- `global_coherence` — **this field is the incoherence degree**, `unsat / union_class_count`
  (0 = clean, higher = worse). The name is misleading; the procedure doc confirms the semantics.

Backend: ROBOT (`--backend robot`, `-Xmx31g`). ELK = sound lower bound
(`unsat_ELK ≤ unsat_HermiT`); HermiT = exact.

## Results

Ranked best (most coherent) to worst within each pair. Degree shown as a percentage
of the merged signature; ELK figures are lower bounds.

### NCIT–DOID — merged signature 231,503

| System | Unsat (ELK) | Degree (ELK) | Unsat (HermiT) | Degree (HermiT) |
|---|---:|---:|---:|---:|
| LogMap | 8 | 0.0035 % | 8 | 0.0035 % |
| BERTMap | 14 | 0.0060 % | 14 | 0.0060 % |
| Naive-Lexical | 9,058 | 3.913 % | 9,153 | 3.954 % |
| BERTMapLt | 10,880 | 4.700 % | 10,971 | 4.739 % |
| LogMapLt | 38,034 | 16.429 % | 38,036 | 16.430 % |
| AML | 64,366 | 27.804 % | 64,371 | 27.806 % |
| *Reference alignment (unrepaired)* | *18,053* | *7.798 %* | *18,145* | *7.838 %* |

### SNOMED–FMA — merged signature 490,694 (ELK only)

| System | Unsat (ELK) | Degree (ELK) |
|---|---:|---:|
| Naive-Lexical | 70,161 | 14.298 % |
| BERTMap | 76,300 | 15.549 % |
| LogMap | 97,408 | 19.851 % |
| BERTMapLt | 127,556 | 25.995 % |
| AML | — not run — | — |
| LogMapLt | — not run — | — |

### SNOMED–NCIT — merged signature 597,931 (ELK only, except LogMapLt)

| System | Unsat (ELK) | Degree (ELK) |
|---|---:|---:|
| LogMap | 448 | 0.0749 % |
| BERTMap | 9,801 | 1.639 % |
| AML | 13,494 | 2.257 % |
| BERTMapLt | 91,671 | 15.331 % |
| Naive-Lexical | 106,147 | 17.752 % |
| LogMapLt | 540,142 | 90.335 % |
| *Reference alignment (unrepaired)* | *466,377* | *77.996 %* |

Naive-Lexical's denominator is 597,932 and the reference's is 597,949 — minor
signature drift between runs, immaterial to the degree.

## Coverage

|  | NCIT–DOID | SNOMED–FMA | SNOMED–NCIT |
|---|:---:|:---:|:---:|
| LogMap | ELK + HermiT | ELK | ELK |
| LogMapLt | ELK + HermiT | **missing** | ELK (+HermiT, see caveat) |
| AML | ELK + HermiT | **missing** | ELK |
| BERTMap | ELK + HermiT | ELK (+HermiT, see caveat) | ELK |
| BERTMapLt | ELK + HermiT | ELK | ELK |
| Naive-Lexical | ELK + HermiT | ELK | ELK |

No coherence data exists for **SapBERT** (despite `baselines/sapbert/` being present),
and none for Matcha or OWL2Vec. Those are local-task systems, so this may be by design.

## Caveats worth knowing before publishing

1. **`bertmap__coherence_global_SNOMED_FMA_scores__HermiT.json` is a mislabelled copy
   of the ELK file** — its body reads `"reasoner_used": "elk", "lower_bound": true`.
   There is no real HermiT run for that cell. Do not cite it as exact.
2. **`LOGMAP_LT__coherence_global_SNOMED_NCIT_scores__HermiT.json` is flagged exact
   (`lower_bound: false`) but returns numbers identical to ELK.** Given the procedure
   doc's own expectation that SNOMED-scale pairs do not terminate under HermiT, treat
   this one as unconfirmed until the run log is checked.
3. **AML and LogMapLt on SNOMED–FMA were scripted but never produced output.** Note
   that `logmap_lt_compute_coherence.sh` points its inputs at
   `/home/jon/new_bioml_workspace/...`, which contains no coherence JSONs — consistent
   with those runs having failed on a bad path.
4. **The `REFERENCE_ALIGNMENT__*` rows are an older snapshot** than this repo's
   `reference_coherence.json`. The authoritative reference figures are in
   `results/coherence/coherence_repair_efficacy.json` (NCIT–DOID 17,850 / 7.710 %;
   SNOMED–NCIT 466,306 / 77.984 %), which match `reference_coherence.json`. The
   ~200-class discrepancy is a snapshot difference, not a contradiction, but the
   efficacy JSON is the one to cite.
5. **SNOMED–FMA has no unrepaired-reference baseline** — the standard merge does not
   classify under ELK within 4 h (`reference_standard__SNOMED-FMA__ELK.TIMEOUT.json`).
6. All SNOMED-pair figures are **ELK lower bounds**. The HermiT–ELK gaps on NCIT–DOID
   are ≤ 95 classes, so the floors are probably tight, but they remain floors.

## Do not confuse with

- `/home/jon/REPAIR_OUTPUTS/coherence_elk/run-*/coh.log` — 46 runs, all
  **reference-alignment repair variants** (consensus2/3, optionB, dcALCOMO, deployed,
  incremental). Directory names like `run-dcref-dcAML-*` mean AML-as-*repair-tool*,
  not AML-as-matcher.
- `/home/jon/REPAIR_OUTPUTS/consensus_reference_tooling/outputs/coherence.json` —
  post-repair reference coherence (all zero), same thing as this repo's
  `reference_coherence.json`.

The original output dir named in `_meta.coherence_dir`
(`work/build-mixed/release/private/coherence/`) is now **empty**; `results/coherence/`
is the surviving copy.
