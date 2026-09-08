# Submission Support

This page collects the fixes for a submission that uploads fine but **scores `0.000` on every pair**, or whose container log reports `scoring failed`. It applies to **both CodaBench competitions** (global alignment and local ranking): they locate your per-pair files in the same way.

**In short:** name each file after its pair slug **with hyphens** (`ncit-doid`, `snomed-fma`, `snomed-ncit`), build the zip from the command line so it carries no hidden macOS metadata, and [check what the scorer will see](#check-what-the-scorer-will-see) before you upload.

## Symptoms

* The upload is accepted, finishes quickly, and every leaderboard column reads `0.000`.
* The submission's container log (*My Submissions → logs*) shows `WARNING: <pair>: scoring failed ('utf-8' codec can't decode byte …); scored zero` for each pair — or shows nothing and simply scores zero.
* An earlier upload of the same files scored normally, but a re-zipped copy does not.

## Cause 1 — macOS Finder adds hidden `__MACOSX` files

When you compress a folder or a selection of files in Finder (right-click → *Compress*), macOS typically adds a hidden `__MACOSX/` directory to the archive holding an AppleDouble sidecar (`._ncit-doid.tsv`, …) beside every real file. The sidecars carry Finder metadata, not your alignment, and they are not valid text.

The scorer unzips your archive and finds each pair's file by walking **every** directory, keeping any file whose name contains the pair slug and ends in an accepted suffix, and taking the **first hit in sorted path order**. A sidecar such as `__MACOSX/final_predictions/._ncit-doid.tsv` passes both tests, so two candidates compete for each pair, and a plain character-code comparison of the two paths decides which wins:

| Your folder or file name starts with… | Sorts relative to `__MACOSX` | Result |
|---|---|---|
| an uppercase letter (`A`–`Z`, codes 0x41–0x5A) | before `_` (0x5F) | your file wins — scores normally |
| a lowercase letter (`a`–`z`, codes 0x61–0x7A) | after `_` (0x5F) | the sidecar wins — scored zero |

So `BIOML_FINAL/ncit-doid.tsv` scores while `final_predictions/ncit-doid.tsv` does not, and a **flat** Finder zip (files at the top level, lowercase names) always fails, because `__MACOSX/._ncit-doid.tsv` sorts before `ncit-doid.tsv`. The scorer then tries to parse the binary sidecar, fails, and records zero for that pair. You can see the sidecars with:

```bash
unzip -l submission.zip
#   __MACOSX/final_predictions/._ncit-doid.tsv    <- hidden sidecar
#   final_predictions/ncit-doid.tsv               <- your file
```

## Cause 2 — the filename does not contain the pair slug

The scorer matches files by the **hyphenated, lowercase** pair slug. A file named `ncit_doid.tsv`, `NCITDOID.tsv` or `pair1.tsv` is never matched, so the pair is scored as an empty alignment — zero, with nothing in the log. Underscores are the usual trap. Letter case is ignored (`NCIT-DOID.tsv` is fine) and extra text is allowed (`my_ncit-doid.tsv` is fine), but keep the hyphen and include **exactly one** file per pair. The simplest names are:

```
ncit-doid.tsv    snomed-fma.tsv    snomed-ncit.tsv      # TSV (either competition)
ncit-doid.rdf    snomed-fma.rdf    snomed-ncit.rdf      # OAEI Alignment RDF (global alignment only)
```

## Fix — build the archive from the command line

Command-line `zip` never writes `__MACOSX/`. From the directory that holds your three files:

```bash
zip -X -j submission.zip ncit-doid.tsv snomed-fma.tsv snomed-ncit.tsv
```

`-j` stores the files at the top level of the archive (no folder) and `-X` drops extended attributes. A folder inside the zip is tolerated, but a flat archive is the safest layout.

Already have a Finder-made zip? Strip the metadata instead of rebuilding:

```bash
zip -d submission.zip '__MACOSX/*' '*.DS_Store'
```

On any platform, without a `zip` binary:

```bash
python3 - <<'EOF'
import zipfile
with zipfile.ZipFile("submission.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for name in ["ncit-doid.tsv", "snomed-fma.tsv", "snomed-ncit.tsv"]:
        z.write(name, arcname=name)
EOF
```

Windows Explorer's *Send to → Compressed (zipped) folder* and Linux archive managers do not add sidecars; the filename rule still applies to them.

## Check what the scorer will see

Run this beside the archive before you upload. It applies the scorer's own discovery rule to the zip listing:

```bash
python3 - submission.zip <<'EOF'
import sys, zipfile
names = zipfile.ZipFile(sys.argv[1]).namelist()
for slug in ["ncit-doid", "snomed-fma", "snomed-ncit"]:
    hits = sorted(n for n in names if slug in n.lower()
                  and n.lower().endswith((".rdf", ".xml", ".owl", ".tsv", ".txt", ".csv")))
    print(f"{slug:12s} -> {hits[0] if hits else 'NOT FOUND'}")
EOF
```

A correct archive prints three lines naming your three files:

```
ncit-doid    -> ncit-doid.tsv
snomed-fma   -> snomed-fma.tsv
snomed-ncit  -> snomed-ncit.tsv
```

`NOT FOUND` means a filename is missing the slug (Cause 2). A path starting `__MACOSX/` means the archive still carries sidecars (Cause 1).

Then validate each file's structure with the scoring kit as usual: [`validate_global.py`](./tasks/global/submission-format.md) for the global alignment, [`validate_ranking.py`](./tasks/local/submission-format.md) for the local ranking.

## Still stuck?

Email [contact@oaei-ml.org](mailto:contact@oaei-ml.org) with the archive listing (`unzip -l submission.zip`) and, if you can, the container log — or open an issue on the [track repository](https://github.com/liseda-lab/OAEI-Bio-ML/issues).
