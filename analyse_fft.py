
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---- Plot configuration ----
# NORM_MODE options:
#   "relative_each"    -> each trace normalised to its own maximum (shape comparison)
#   "relative_input30" -> both traces referenced to the INPUT magnitude at 30 kHz
#   "absolute"         -> raw FFT magnitudes in dB (no extra normalisation)
NORM_MODE = "relative_each"
PASS_TONE_HZ = 30_000.0  # frequency to highlight (30 kHz)

# Circle styling (scatter uses area in points^2)
CIRCLE_SIZE_PT2 = 600   # increase for a larger ring (e.g., 600–1200)
CIRCLE_EDGE_LW  = 2.0   # thicker edge for visibility

# ---------- Load and clean ----------
df = pd.read_csv("sim_io.csv")      # the csv file which was created while running the Vivado Simulation
_din  = pd.to_numeric(df.iloc[:, 1], errors="coerce")
_dout = pd.to_numeric(df.iloc[:, 2], errors="coerce")
mask  = ~_din.isna() & ~_dout.isna()

din  = _din[mask].to_numpy(dtype=float) / 8192.0
dout = _dout[mask].to_numpy(dtype=float) / 8192.0

FS = 1_000_000.0
N_MAX = 8192
N = int(min(N_MAX, len(din), len(dout)))
w = np.hanning(N)

DIN  = np.fft.rfft(din[:N]*w)
DOUT = np.fft.rfft(dout[:N]*w)
freqs = np.fft.rfftfreq(N, 1/FS)

# ---- Fig A: Input vs Output spectra in dB ----
EPS = 1e-20
mag_db = lambda z: 20*np.log10(np.abs(z)+EPS)

DIN_dB  = mag_db(DIN)
DOUT_dB = mag_db(DOUT)

# Choose normalisation
if NORM_MODE == "relative_each":
    y_in  = DIN_dB  - np.max(DIN_dB)
    y_out = DOUT_dB - np.max(DOUT_dB)
    y_label = "Magnitude (dB)"
elif NORM_MODE == "relative_input30":
    idx30 = int(np.argmin(np.abs(freqs - PASS_TONE_HZ)))
    ref = DIN_dB[idx30]  # reference = input magnitude at 30 kHz
    y_in  = DIN_dB  - ref
    y_out = DOUT_dB - ref
    y_label = "Magnitude (dB, referenced to input @ 30 kHz)"
else:  # "absolute"
    y_in, y_out = DIN_dB, DOUT_dB
    y_label = "Magnitude (dB)"

plt.figure(figsize=(7.2,4.2))
plt.plot(freqs/1e3, y_in,  label="Input")
plt.plot(freqs/1e3, y_out, label="Output")
plt.xlabel("Frequency (kHz)")
plt.ylabel(y_label)
plt.title(f"Input vs Output Spectrum (Zoomed)")
plt.grid(True, ls=":")
plt.xlim(0, 60)
plt.ylim(-80, 5)
plt.legend()

# --- Circle/annotate the 30 kHz peak on the OUTPUT trace ---
idx30 = int(np.argmin(np.abs(freqs - PASS_TONE_HZ)))
x30 = freqs[idx30]/1e3
y30 = y_out[idx30]
plt.scatter([x30],[y30], s=CIRCLE_SIZE_PT2, facecolors="none",
            edgecolors="crimson", linewidths=CIRCLE_EDGE_LW, zorder=10)

plt.tight_layout()


# ---- Optional: stem plot at the five tone frequencies ----
# Pre-compute per-bin difference (used for per-tone gain only)
Diff_dB = mag_db(DOUT) - mag_db(DIN)
tone_khz = np.array([10, 20, 30, 40, 50])
tone_hz  = 1e3 * tone_khz
idx = [int(np.argmin(np.abs(freqs - f))) for f in tone_hz]
plt.figure(figsize=(6.4,3.6))
# Call stem() in a way that works for both old and new Matplotlib
try:
    stem_ret = plt.stem(tone_khz, Diff_dB[idx], use_line_collection=True)
except TypeError:
    # Older Matplotlib doesn't support the keyword
    stem_ret = plt.stem(tone_khz, Diff_dB[idx])

# Unpack robustly (old versions return a tuple; newer return a StemContainer)
try:
    markerline, stemlines, baseline = stem_ret
except Exception:
    markerline = getattr(stem_ret, "markerline", None)
    stemlines  = getattr(stem_ret, "stemlines", None)
    baseline   = getattr(stem_ret, "baseline", None)

if stemlines is not None:
    plt.setp(stemlines, linewidth=2)
if markerline is not None:
    plt.setp(markerline, markersize=6)
plt.axhline(0, color='k', lw=0.8, ls='--', alpha=0.6)
plt.xlabel("Frequency (kHz)")
plt.ylabel("Δ Magnitude (dB)")
plt.title("Per-Tone Gain: Output − Input (dB)")
plt.grid(True, ls=":")
plt.ylim(min(-60, np.min(Diff_dB[idx])-5), max(10, np.max(Diff_dB[idx])+5))
plt.tight_layout()

plt.show()

