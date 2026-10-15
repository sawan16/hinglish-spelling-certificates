Hinglish Spelling Certificates
Code, results and the Hinglish spelling-variant lexicon for the paper:
> **Exact Robustness Certificates for Hinglish Text Classification under Romanized Spelling Variation**
> (submitted to ACM Transactions on Asian and Low-Resource Language Information Processing)
Romanized Hindi has no standard spelling. The same word can be written nahi, nahin or nai. This repository shows that worst-case respelling within such variants changes the decisions of fine-tuned Hinglish classifiers. It also provides exact, distribution-free certificates for classifiers composed with a token-wise canonicalizer.
Repository layout
Path	Contents
`code/hinglish_certified_experiments.ipynb`	Every experiment in the paper: 40 runs (2 datasets × 3 encoders × 4 canonicalizers; 3 seeds for HingRoBERTa). Resumable; runs on one T4/P100 GPU (Kaggle or Colab).
`code/fill_results.py`	Builds the LaTeX tables from the results folder
`code/make_figure.py`	Builds the figure (gap vs. number of rewritable tokens)
`code/lexicon/hinglish_variants_R.tsv`	Lexicon R: 49,090 attested romanizations in 29,004 variant classes (from Dakshina)
`code/lexicon/hinglish_variants_Rplus.tsv`	Lexicon R+: R plus five phonetic rules, 164,646 romanizations
`results/results/runs/`	Per-run predictions, worst-case outcomes and conformal sets (`.npz`, `.json`)
`results/results/tables/`	`all_runs.csv`, resource statistics and table sources
`results/results/figures/`	Figure output
Lexicon format
The lexicon files are tab-separated, with one romanization per line:
```
class_id    romanization    weight
सिस्टम       system          10.0
```
`class_id` is the Devanagari word that defines the variant class.
`weight` is the Dakshina attestation count.
Two strings are declared variants exactly when they share a `class_id`.
Reproducing the paper
Open `code/hinglish_certified_experiments.ipynb` on Kaggle or Colab with a GPU.
Provide the SentiMix zip. Either let the notebook download it, or set `SENTIMIX_LOCAL` to an uploaded copy if Zenodo times out.
Run all cells. A completed run is skipped on restart, and the notebook writes `paper_results.zip` at the end.
Build the tables and the figure:
```bash
   python code/fill_results.py results/results tex/
   python code/make_figure.py  results/results tex/figures
   ```
The full grid takes roughly 3–4 GPU hours. Batched fp16 inference can change a handful of individual decisions between hardware types; the paper reports the size of this effect.
Data sources
None of these datasets is redistributed here. The notebook downloads them from the original sources.
SemEval-2020 Task 9 SentiMix (Hindi–English): Zenodo record 3974927, CC BY 4.0.
Hinglish sarcasm corpus (Swami et al., 2018): https://github.com/sahilswami96/SarcasmDetection_CodeMixed, GPL-3.0.
Dakshina v1.0 Hindi lexicons (Roark et al., 2020): CC BY-SA 4.0.
Licence
Code (`code/*.ipynb`, `code/*.py`): MIT licence; see `LICENSE`.
Lexicon (`code/lexicon/`): CC BY-SA 4.0, inherited from Dakshina; see `code/lexicon/LICENSE`.
Results (`results/`): CC BY 4.0.
Citation
If you use the code or the lexicon, please cite the paper. A BibTeX entry will be added on publication.
