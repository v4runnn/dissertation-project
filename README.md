# Dissertation Project – FPGA-Based Design and Simulation of a Linear Feedback Controller for Levitated Nanoparticles 

This repository contains the source code, simulations, and analysis used in my dissertation project.  
It combines **MATLAB**, **Python**, and **Verilog (Vivado)** to design, simulate, and evaluate a Linear Feedback Controller in FPGA.

---

## 📂 Repository Contents
 
### Python Scripts
- **`make_arb_sines.py`**  
  Generates a CSV waveform for Red Pitaya Arbitrary Waveform Generator.  
  - Sum of five sine waves (default: 10, 20, 30, 40, 50 kHz).  
  - Normalised to ±1 and saved as `arb_sines.csv`.
    
- **`get_filter_coeffs.py`**  
  Computes IIR biquad bandpass filter coefficients (RBJ form).  
  - Parameters: sampling rate, centre frequency, Q-factor.  
  - Exports both floating-point and fixed-point (Q14) coefficients.  
  - Prints Verilog-ready `parameter` definitions.
 
  - **`analyse_fft.py`**  
  Loads Vivado simulation results (`sim_io.csv`) and performs FFT analysis.  
  - Compares spectra of input vs. output signals.  
  - Highlights passband tone (30 kHz by default).  
  - Produces plots of per-tone gain.

### MATLAB Code
- **`Filter_Testing.m`**  
  Standalone MATLAB script that designs and verifies the bandpass filter before hardware implementation.  
  - Sampling frequency: 1 MHz (matches the simulation testbench).  
  - Designs a 2nd-order bandpass filter centred at 30 kHz with Q ≈ 3.  
  - Normalises coefficients and computes the frequency response.  
  - Plots the magnitude response (0–100 kHz).  
  - Serves as an early **verification reference** before Verilog simulation.

### Vivado Simulation
- **`RedPitaya_LinearFeedbackController w BandPass (Simulation).zip`**  
  Contains Verilog source files, testbenches, and Vivado simulation setup.  
  - Implements the linear feedback controller with the bandpass filter.  
  - Generates `sim_io.csv`, later analysed with Python.

---

## 📊 Workflow Overview

1. **Python (`make_arb_sines.py`)** → Generate multi-tone input waveform.  
2. **Python (`get_filter_coeffs.py`)** → Generate fixed-point coefficients for Verilog.
3. **MATLAB (`test_filter.m`)** → Design and verify bandpass filter response.
4. **Verilog (Vivado project)** → Implement and simulate the Controller.  
5. **Python (`analyse_fft.py`)** → Analyse simulation results (FFT, per-tone gain).  
6. **(Optional)** Deploy waveform to Red Pitaya hardware for real measurements.

---

## 🛠️ Requirements
- MATLAB (tested with R2024b)  
- Python 3.8+ with packages:  
  - `numpy`  
  - `pandas`  
  - `matplotlib`  
- Xilinx Vivado 2020.1 (for Verilog simulation)  

---
