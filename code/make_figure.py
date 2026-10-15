"""Figure: clean minus worst-case accuracy vs number of rewritable Hindi tokens (HingRoBERTa, 3 seeds pooled)."""
import sys, os, glob, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
res, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#888888",
                     "axes.labelcolor": "#333333", "xtick.color": "#555555", "ytick.color": "#555555", "pdf.fonttype": 42})
SER = [("raw", "R", "raw, threat $R$", "#2a78d6", "o", "-"),
       ("raw", "Rp", "raw, threat $R^{+}$ (lower bound)", "#eb6834", "s", "-"),
       ("lexRp", "Rp", r"\textsc{lexR+}".replace(r"\textsc{lexR+}", "lexR+") + ", threat $R^{+}$", "#1baf7a", "^", "--")]
bins = [0, 1, 3, 5, 8, 12, 10**6]; lab = ["0", "1–2", "3–4", "5–7", "8–11", "12+"]
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.7), sharey=False)
for ax, d, title in zip(axes, ["sentimix", "sarcasm"], ["SentiMix (sentiment)", "Sarcasm"]):
    for c, th, name, col, mk, ls in SER:
        A = [np.load(f) for f in sorted(glob.glob(f"{res}/runs/{d}__hingroberta__{c}__s*.npz"))]
        ne = np.concatenate([a["n_elig_Rp"] for a in A])
        gap = np.concatenate([(a["y"] == a["pred"]).astype(float) - a[f"robust_{th}"] for a in A])
        b = np.digitize(ne, bins[1:-1])
        ys = [100 * gap[b == k].mean() if (b == k).sum() >= 30 else np.nan for k in range(len(lab))]
        ax.plot(lab, ys, ls, color=col, marker=mk, markersize=5, linewidth=2, label=name)
    ax.set_title(title, fontsize=10, color="#222222"); ax.set_xlabel("rewritable Hindi tokens in text ($R^{+}$)")
    ax.grid(axis="y", color="#e6e6e6", linewidth=0.8); ax.set_axisbelow(True)
axes[0].set_ylabel("clean − worst-case acc. (pts)")
axes[0].legend(frameon=False, fontsize=8, loc="upper left")
plt.tight_layout()
for ext in ("pdf", "png"): plt.savefig(f"{out}/gap_vs_tokens.{ext}", dpi=200)
print("saved")
