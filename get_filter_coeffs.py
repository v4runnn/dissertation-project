import math

# ----------------------------
# Inputs you change
# ----------------------------
FS_HZ = 1_000_000        # sampling rate (Hz)
F0_HZ = 30_000           # bandpass center (Hz)
Q      = 3.0             # quality factor  (bandwidth ~ F0/Q)
# Optional: set this to True if you want unity |H(e^jw0)| exactly
FORCE_UNITY_AT_F0 = True

# ----------------------------
# RBJ “constant skirt gain, peak gain = Q” bandpass
# ----------------------------
w0 = 2.0 * math.pi * (F0_HZ / FS_HZ)           # rad/sample
alpha = math.sin(w0) / (2.0 * Q)

b0 =  alpha
b1 =  0.0
b2 = -alpha
a0 =  1.0 + alpha
a1 = -2.0 * math.cos(w0)
a2 =  1.0 - alpha

# Normalize so a0 = 1 (what your Verilog expects)
b0n = b0 / a0
b1n = b1 / a0
b2n = b2 / a0
a1n = a1 / a0
a2n = a2 / a0

# Optionally tweak overall gain so |H| = 1 exactly at F0
if FORCE_UNITY_AT_F0:
    # H(e^jw) at w0
    ejw  = complex(math.cos(w0), math.sin(w0))
    ejw2 = complex(math.cos(2*w0), math.sin(2*w0))
    num  = b0n + b1n*ejw**-1 + b2n*ejw**-2
    den  = 1.0 + a1n*ejw**-1 + a2n*ejw**-2
    g = abs(num/den)
    if g != 0.0:
        b0n /= g; b1n /= g; b2n /= g

# ----------------------------
# Convert to signed Q14 (fits in 16-bit)
# ----------------------------
def to_q14(x):
    s = int(round(x * (1<<14)))
    # clamp to int16 range
    return max(min(s,  32767), -32768)

B0_Q14 = to_q14(b0n)
B1_Q14 = to_q14(b1n)
B2_Q14 = to_q14(b2n)
A1_Q14 = to_q14(a1n)
A2_Q14 = to_q14(a2n)

print("Biquad (Fs={} Hz, f0={} Hz, Q={}):".format(FS_HZ, F0_HZ, Q))
print("  float:  b0={:+.6f}  b1={:+.6f}  b2={:+.6f}  a1={:+.6f}  a2={:+.6f}"
      .format(b0n, b1n, b2n, a1n, a2n))
print("  Q14  :  B0_Q14={:+d}  B1_Q14={:+d}  B2_Q14={:+d}  A1_Q14={:+d}  A2_Q14={:+d}"
      .format(B0_Q14, B1_Q14, B2_Q14, A1_Q14, A2_Q14))

print("\n// Paste these into biquad_bandpass_fixed #(...)")
print("parameter signed [15:0] B0_Q14 = 16'sd{};".format(B0_Q14))
print("parameter signed [15:0] B1_Q14 = 16'sd{};".format(B1_Q14))
print("parameter signed [15:0] B2_Q14 = 16'sd{};".format(B2_Q14))
print("parameter signed [15:0] A1_Q14 = 16'sd{};".format(A1_Q14))
print("parameter signed [15:0] A2_Q14 = 16'sd{};".format(A2_Q14))
