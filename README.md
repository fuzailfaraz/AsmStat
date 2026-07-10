# AsmStat - Dual Architecture Statistical Engine 🚀

**AsmStat** is a comprehensive dual-architecture data science platform that bridges the gap between low-level hardware programming and modern, interactive web interfaces. This project demonstrates proficiency in **modern 64-bit Assembly** integrated with Python, as well as **retro 16-bit DOS Assembly** using EMU8086.

By developing two distinct engines and bridging them via file synchronization, this project showcases a deep understanding of computer architecture, ABI (Application Binary Interface), memory management, cloud-native deployments, and modern Exploratory Data Analysis (EDA).

---

## 🌟 Part 1: AsmStat Pro Max (Modern 64-bit & Python Web App)

The modern iteration of the project utilizes a high-performance **64-bit Assembly backend** combined with a premium, glassmorphism-styled **Python Streamlit frontend**.

### Key Features:
- **64-bit NASM Backend**: Core statistical operations (Sum, Mean, Variance, StdDev, Min, Max, Dot Product) written in pure 64-bit x86-64 assembly. Includes both `math.asm` (Microsoft x64 ABI for Windows) and `math_linux.asm` (System V AMD64 ABI for Linux/Cloud).
- **Automated Cloud CI/CD Pipeline**: The Python frontend includes a runtime sub-process compiler that automatically invokes `nasm` and `ld` with strict W^X non-executable stack flags (`-z noexecstack`) to build the `.so` library on-the-fly for Streamlit Cloud.
- **Premium Glassmorphism UI**: Built with a multi-page router, custom CSS, the "Outfit" Google Font, and animated glowing metric cards that rival modern JavaScript/React applications.
- **Full Data Science Suite**: Integrates `plotly`, `pandas`, and `openpyxl` to perform rigorous EDA:
  - Supports `.csv`, `.xlsx`, and `.xls` uploads with robust character encoding fallbacks.
  - Interactive Pearson correlation heatmaps, missing value bar charts, and scatter pairplots.
  - Deep-dive column analysis, IQR anomaly detection (outliers), ECDF step distributions, Cumulative Sums, and Moving Averages.

### How to Run:
1. Ensure you have NASM and GCC/ld installed.
2. Run the build script to compile the Windows library (optional on Linux as it compiles at runtime):
   ```bash
   build.bat
   ```
3. Install the Python requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the Streamlit web application:
   ```bash
   streamlit run app.py
   ```

---

## 💾 Part 2: AsmStat Classic (16-bit EMU8086 Edition)

The retro iteration of the project is a standalone, interactive Command Line Interface (CLI) application written entirely in **16-bit DOS Assembly** for the EMU8086 emulator.

### Key Features:
- **Pure 16-bit Environment (`AsmStat.asm`)**: Uses legacy 16-bit registers (`AX`, `BX`, `CX`) and DOS interrupts.
- **VGA Memory Mapping**: Directly writes to the VGA video memory (`0B800h`) to colorize the ASCII art and terminal interface without external libraries.
- **Dynamic Array Handling**: Allows the user to dynamically input array lengths and elements, manipulating memory pointers (`SI`, `DI`) in real-time.
- **Live UI Synchronization**: Exports data straight from the 16-bit processor cache to a `DATA.TXT` file, which is actively polled by the Python web UI to generate modern visualizations of 16-bit inputs.

### How to Run:
1. Open the **EMU8086** IDE.
2. Open the `AsmStat.asm` file.
3. Click the **Emulate** button, then click **Run**.
4. Use the keyboard to navigate the colored menu and perform calculations!

---

## 🧠 Educational Value & Technical Achievements
*   **Cross-Architecture Expertise**: Demonstrates the massive differences between 16-bit segmented real mode and modern 64-bit flat memory models, handling both Windows and Linux Calling Conventions.
*   **Foreign Function Interfaces (FFI)**: Proves the ability to interface high-level scripting languages (Python) with low-level machine code via shared libraries (`.dll` and `.so`) and `ctypes`.
*   **Production Deployment Hardening**: Addressed Linux security policies by manually injecting `.note.GNU-stack` ELF sections to prevent executable stack memory violations on cloud containers.
*   **Data Science Pipeline Automation**: Built robust multi-encoding dataset parsing for reliable analysis of unstructured user data.
