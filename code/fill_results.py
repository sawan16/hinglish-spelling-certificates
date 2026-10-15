"""Fill paper tables from paper_results.zip (or an extracted results dir).
Usage: python fill_results.py <results_dir> <tex_dir>
Writes tex_dir/tables/*.tex and tex_dir/figures/*, and prints headline numbers for the text."""
import sys, os, json, shutil, pandas as pd, numpy as np

res, tex = sys.argv[1], sys.argv[2]
os.makedirs(f"{tex}/tables", exist_ok=True); os.makedirs(f"{tex}/figures", exist_ok=True)
R = pd.read_csv(f"{res}/tables/all_runs.csv")
MODEL = {"hingroberta": "HingRoBERTa", "xlmr": "XLM-R", "muril": "MuRIL"}
CAN = {"raw": "raw", "lexR": "\\textsc{lexR}", "lexRp": "\\textsc{lexR+}", "lex_train": "\\textsc{lexTrain}"}
DS = {"sentimix": "SentiMix", "sarcasm": "Sarcasm"}
order_m = [m for m in MODEL if m in R.model.unique()]; order_c = ["raw", "lexR", "lexRp"]

def write_table(tex, name, spec, header, rows):
    body = "\n".join(rows)
    open(f"{tex}/tables/{name}_table.tex", "w").write(
        f"\\begin{{tabular}}{{{spec}}}\n\\toprule\n{header}\\\\\n\\midrule\n{body}\n\\bottomrule\n\\end{{tabular}}\n")

def cell(g, col):
    m, s, n = 100 * g[col].mean(), 100 * g[col].std(), len(g)
    return f"{m:.1f}" + (f"$\\pm${s:.1f}" if n > 1 and not np.isnan(s) else "")

def cellb(g, col, ex):
    # value with dagger when not all texts were enumerated exactly (then robust acc / coverage is an upper bound)
    return cell(g, col) + ("$^\\dagger$" if g[ex].mean() < 0.999 else "")

# Table 2: main
rows = []
for d in DS:
    first = True
    for m in order_m:
        for c in order_c:
            g = R[(R.dataset == d) & (R.model == m) & (R.canon == c)]
            if g.empty: continue
            rows.append(f"{DS[d] if first else ''} & {MODEL[m]} / {CAN[c]} & {cell(g,'acc_clean')} & {cell(g,'f1_clean')} & {cell(g,'acc_natural')} & "
                        f"{cellb(g,'robust_acc_R','exact_share_R')} & {cellb(g,'robust_acc_Rp','exact_share_Rp')} & {cellb(g,'robust_bacc_Rp','exact_share_Rp')}\\\\")
            first = False
    rows.append("\\midrule")
write_table(tex, "main", "llcccccc", "Data & Model / canon. & Acc & Macro-F1 & Natural & Worst $R$ & Worst $R^{+}$ & Bal.\\ worst $R^{+}$", rows[:-1])

# Table 3: certification and audit under threat R (lexR: invariant; lexTrain: leaky -> hybrid)
rows = []
for d in DS:
    first = True
    for m in order_m:
        for c in ["lexR", "lex_train"]:
            g = R[(R.dataset == d) & (R.model == m) & (R.canon == c)]
            if g.empty: continue
            rows.append(f"{DS[d] if first else ''} & {MODEL[m]} / {CAN[c]} & {cell(g,'acc_clean')} & {cellb(g,'robust_acc_R','exact_share_R')} & {cell(g,'leak_rate_R')} & {cell(g,'leak_ucb_R')} & "
                        f"{cell(g,'audit_lcb_R')} & {g['orbit_median_R'].mean():.0f} / {g['orbit_p95_R'].mean():.0f}\\\\")
            first = False
    rows.append("\\midrule")
write_table(tex, "hybrid", "llcccccc", "Data & Model / canon. & Acc & Worst $R$ & Leak & Leak UCB & Audit LCB & Cost med / p95", rows[:-1])

# Table 4: conformal
rows = []
for d in DS:
    first = True
    for m in order_m:
        for c in ["raw", "lexRp"]:
            g = R[(R.dataset == d) & (R.model == m) & (R.canon == c)]
            if g.empty: continue
            rows.append(f"{DS[d] if first else ''} & {MODEL[m]} / {CAN[c]} & {cell(g,'cov_clean')} & {cellb(g,'cov_worst_R','exact_share_R')} & {cellb(g,'cov_worst_Rp','exact_share_Rp')} & {g['setsize_clean'].mean():.2f}\\\\")
            first = False
    rows.append("\\midrule")
write_table(tex, "conformal", "llcccc", "Data & Model / canon. & Cov.\\ clean & Cov.\\ worst $R$ & Cov.\\ worst $R^{+}$ & Set size", rows[:-1])

# Table 1: resource
st = json.load(open(f"{res}/tables/resource_stats.json")); L = st["lexicon"]; cov = pd.DataFrame(st["coverage"])
r1 = [f"$R$ & {L['R']['spellings']:,} & {L['R']['classes']:,} & {L['R']['mean_class']:.2f} & {100*L['R']['share_multi']:.1f}\\%\\\\",
      f"$R^{{+}}$ & {L['R+']['spellings']:,} & {L['R+']['classes']:,} & {L['R+']['mean_class']:.2f} & {100*L['R+']['share_multi']:.1f}\\%\\\\"]
r2 = [f"{DS[x.dataset]} / {'$R$' if x.threat=='R' else '$R^{+}$'} & {int(x.hindi_tokens):,} & {100*x.in_lexicon:.1f}\\% & {100*x['with_>=2_spellings']:.1f}\\% & {x.median_rewritable_per_test_text:.0f}\\\\"
      for _, x in cov.iterrows()]
write_table(tex, "resource", "lrrrr", "Relation & Spellings & Classes & Mean class size & Classes with $\\ge2$ spellings",
            r1 + ["\\midrule", "Dataset / relation & Hindi tokens & In lexicon & Multi & Median rewritable per text\\\\", "\\midrule"] + r2)

# figure is produced by make_figure.py

# Headline numbers
H = {}
for d in DS:
    for m in order_m:
        raw = R[(R.dataset == d) & (R.model == m) & (R.canon == "raw")]; inv = R[(R.dataset == d) & (R.model == m) & (R.canon == "lexRp")]
        if raw.empty: continue
        H[f"{d}/{m}"] = {"clean": 100 * raw.acc_clean.mean(), "natural_drop": 100 * (raw.acc_clean - raw.acc_natural).mean(),
                         "worstR_drop": 100 * (raw.acc_clean - raw.robust_acc_R).mean(), "worstRp_drop": 100 * (raw.acc_clean - raw.robust_acc_Rp).mean(),
                         "inv_cost": 100 * (raw.acc_clean.mean() - inv.acc_clean.mean()) if not inv.empty else None,
                         "inv_robust_eq_clean": bool(np.allclose(inv.robust_acc_Rp, inv.acc_clean)) if not inv.empty else None}
print(json.dumps(H, indent=1, default=float))
json.dump(H, open(f"{tex}/tables/headline.json", "w"), indent=1, default=float)
