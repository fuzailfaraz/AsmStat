# Software Reference Document (SRD)
**Project:** AsmStat Pro
**Version:** 2.0.0
**Target Environment:** Windows (Local), Linux (Streamlit Cloud)

---

## 1. System Architecture
AsmStat Pro uses a Hybrid Architecture consisting of three distinct layers:
1.  **Frontend Layer (Python/Streamlit):** Handles UI rendering, user interaction, state routing, dataset ingestion, and visual analytics (Plotly).
2.  **Foreign Function Interface (Python/ctypes):** Acts as the bridge, mapping Python arrays to raw C-pointers and invoking dynamic library symbols.
3.  **Low-Level Compute Engine (x86-64 Assembly):** The native backend that processes integer arithmetic at the hardware level.

### 1.1 Compute Engine Specifications
The compute engine exists in two variants to satisfy cross-platform Calling Conventions (ABI):
-   **`math.asm` (Windows):** Follows the Microsoft x64 Calling Convention (`RCX`, `RDX`, `R8`, `R9`). Generates `math.dll`.
-   **`math_linux.asm` (Linux):** Follows the System V AMD64 ABI (`RDI`, `RSI`, `RDX`, `RCX`, `R8`, `R9`). Generates `libmath.so`. Includes `.note.GNU-stack` to strictly comply with W^X memory protection.

## 2. Core Modules & Files

### 2.1 `app.py`
The primary entry point of the web application. 
-   **Page Routing:** Implements a session-state based router to toggle between the `🏠 Home` view and `📊 Analytics Engine` view.
-   **Runtime Compiler (`_build_linux_library`):** A fallback compilation pipeline that detects Linux environments, executes `nasm -f elf64` and `ld -shared -z noexecstack`, and generates the shared object if it is missing or stale compared to source files.
-   **Data Ingestion Pipeline:** Uses `pandas` to read datasets. Implements an automatic `utf-8` → `latin1` → `cp1252` encoding fallback loop for robust CSV decoding. Supports `.xlsx` and `.xls` via `openpyxl`.
-   **EDA Submodule:** Dynamically charts Missing Values, Correlation Heatmaps, Pairplots (Splom), and Individual Column metrics.

### 2.2 Assembly Routines (Backend)
Both `math.asm` and `math_linux.asm` expose the following globally accessible labels:
-   `asm_sum`: Iterates through a 64-bit integer array. Returns total sum.
-   `asm_mean`: Calls `asm_sum` and performs integer division (`IDIV`) by array length.
-   `asm_variance`: Computes `(x - mean)^2 / N` iteratively.
-   `asm_stddev`: Relies on the FPU (`fild`, `fsqrt`, `fstp`) or modern SSE registers (`cvtsi2sd`, `sqrtsd`) to return a `double` precision floating point value.
-   `asm_dot_product`: Takes two array pointers, sequentially multiplies corresponding elements, and accumulates the total.

### 2.3 `AsmStat.asm` (16-Bit EMU8086)
A completely separate CLI application meant for retro education.
-   Directly accesses VGA video memory (`0xB800`) for text coloring.
-   Implements Bubble Sort and basic arithmetic via 16-bit registers.
-   Synchronizes outputs to `DATA.txt` on the local drive, acting as an IoT-like data stream for the Python frontend.

## 3. Dependency Graph
-   **Python >= 3.9**
    -   `streamlit`: UI Framework
    -   `pandas`, `numpy`: Data manipulation
    -   `plotly`: Interactive visual graphing
    -   `openpyxl`, `xlrd`: Excel file parsing support
-   **System Utilities**
    -   `nasm`: The Netwide Assembler (for building `.o` object files).
    -   `ld` (binutils): GNU linker (for creating shared libraries).

## 4. Deployment Pipeline (Streamlit Cloud)
To bypass immutable container environments on Streamlit Cloud:
1.  `packages.txt` is read by the Debian package manager (`apt-get`), installing `nasm` and `binutils`.
2.  `requirements.txt` installs Python dependencies.
3.  On launch, `app.py` detects Linux via `platform.system()`.
4.  If `libmath.so` is missing, it triggers the `subprocess` compiler pipeline.
5.  `ctypes.CDLL()` loads the newly compiled binary in memory.
