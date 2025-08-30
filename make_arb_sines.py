# make_arb_sines.py
# Creates a single-column CSV for Red Pitaya ARB with five sine waves.
# Output values are explicitly in ±x.xxx format for WebUI compatibility.

from fractions import Fraction
import numpy as np
import pandas as pd

# -------------------------
# USER SETTINGS
# -------------------------
FREQS_HZ = [10000.0, 20000.0, 30000.0, 40000.0, 50000.0]  # frequencies in Hz
AMPS =     [0.4,    0.3,    0.2,    0.15,   0.1   ]  # relative amplitudes
PHASES_DEG = [0.0,    0.0,    0.0,    0.0,    0.0   ]  # start phases in degrees

DC_OFFSET = 0.0         # constant offset (will also be normalised)
N_SAMPLES = 8192        # number of samples in the CSV
MAX_DENOM = 1000        # integer-cycle match precision
OUTPUT_CSV = "arb_sines.csv"
# -------------------------

def choose_duration_for_integer_cycles(freqs, max_denom=1000):
    """
    Choose a duration T so that all f_i * T are integers.
    We do this by finding ratios relative to the first frequency
    and combining their denominators.
    """
    base_f = freqs[0]
    denominators = []
    numerators = []
    
    for f in freqs:
        ratio = Fraction(f / base_f).limit_denominator(max_denominator=max_denom)
        numerators.append(ratio.numerator)
        denominators.append(ratio.denominator)
    
    # LCM of denominators = cycles of base_f in one period
    from math import lcm
    q = 1
    for d in denominators:
        q = lcm(q, d)
    
    T = q / base_f
    return T

def main():
    # Pick a duration that makes all sines end at zero-crossing
    T = choose_duration_for_integer_cycles(FREQS_HZ, MAX_DENOM)

    # Make a time vector
    t = np.linspace(0.0, T, N_SAMPLES, endpoint=False)

    # Build the sum of sines
    y = np.zeros_like(t)
    for f, a, ph_deg in zip(FREQS_HZ, AMPS, PHASES_DEG):
        ph_rad = np.deg2rad(ph_deg)
        y += a * np.sin(2 * np.pi * f * t + ph_rad)
    
    y += DC_OFFSET

    # Normalise to ±1
    peak = np.max(np.abs(y))
    norm = y / peak if peak != 0 else y

    # Round to 3 decimals
    norm = np.round(norm, 3)

    # Format with explicit ±
    formatted = [f"{value:+.3f}" for value in norm]

    # Save CSV
    pd.DataFrame(formatted).to_csv(
        OUTPUT_CSV,
        index=False,
        header=False
    )

    # Info printout
    print(f"Saved: {OUTPUT_CSV}")
    print(f"Duration T = {T:.9f} s")
    print("Set ARB Frequency in WebUI to {:.6f} Hz for exact output frequencies.".format(1.0 / T))

if __name__ == "__main__":
    main()

# To run this file:
# 1. Type cd "<path_to_your_script>"
# 2. Type python3 make_arb_sines.py