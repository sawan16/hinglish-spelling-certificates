# Hinglish spelling-variant certificates: code and data

This repository accompanies *Exact Robustness Certificates for Hinglish Text Classification under Romanized Spelling Variation*.

## Contents
| File | Description |
|---|---|
| `hinglish_certified_experiments.ipynb` | Every experiment in the paper (Colab T4, about 2.5–3 hours, resumable) |
| `fill_results.py` | Turns `paper_results.zip` into the LaTeX tables and figures |
| `lexicon/hinglish_variants_R.tsv` | Attested spelling-variant classes (from Dakshina) |
| `lexicon/hinglish_variants_Rplus.tsv` | Attested classes plus five phonetic rules |
| `paper/` | LaTeX source (`main_acm.tex` for submission, `main_preview.tex` for a plain-article build) |

## Data sources (downloaded by the notebook)
- **SemEval-2020 Task 9 SentiMix (Hinglish):** Zenodo record 3974927, CC BY 4.0.
- **Swami et al. (2018) Hinglish sarcasm corpus:** github.com/sahilswami96/SarcasmDetection_CodeMixed, GPL-3.0.
- **Dakshina v1.0 Hindi lexicons:** CC BY-SA 4.0.

## Lexicon licence
The variant lexicon is derived from Dakshina, so it is released under **CC BY-SA 4.0**.

## Reproduce
1. Open the notebook in Colab, select a T4 GPU and set `USE_DRIVE = True`.
2. Run all, which writes `paper_results.zip`.
3. Run `python fill_results.py <extracted results dir> paper/`.
4. Compile `paper/main_acm.tex` (Overleaf with acmart) or `paper/main_preview.tex`.

## Citation
Add the BibTeX entry here after acceptance.
