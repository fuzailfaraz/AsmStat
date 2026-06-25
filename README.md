# AsmStat - Dual Architecture Statistical Engine 🚀

**AsmStat** is a comprehensive semester project that bridges the gap between low-level hardware programming and modern, interactive web interfaces. This project demonstrates proficiency in both **modern 64-bit Assembly** integrated with Python, as well as **retro 16-bit DOS Assembly** using EMU8086.

By developing two distinct engines, this project showcases a deep understanding of computer architecture, ABI (Application Binary Interface), memory management, and full-stack integration.

---

## 🌟 Part 1: AsmStat Pro Max (Modern 64-bit & Python Web App)

The modern iteration of the project utilizes a high-performance **64-bit Assembly backend** combined with a beautiful **Python Streamlit frontend**.

### Features:
- **64-bit NASM Backend (`math.asm`)**: Core statistical operations (Sum, Mean, Variance, Min, Max) written in pure 64-bit x86-64 assembly using the Microsoft x64 Calling Convention.
- **Python Integration (`app.py`)**: Uses Python's `ctypes` library to seamlessly load the Assembly DLL and execute native machine code directly from the web app.
- **Interactive UI**: Built with Streamlit, featuring a massive, premium dark-mode interface.
- **Data Visualization**: Integrates `plotly` to dynamically generate Bar Charts, Trend Lines, Box Plots, and Histograms based on the Assembly engine's output.

### How to Run:
1. Ensure you have NASM and GCC installed (or MSVC).
2. Run the build script to compile the Assembly code into a shared library:
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

### Features:
- **Pure 16-bit Environment (`AsmStat.asm`)**: Uses legacy 16-bit registers (`AX`, `BX`, `CX`) and DOS interrupts.
- **VGA Memory Mapping**: Directly writes to the VGA video memory (`0B800h`) to colorize the ASCII art and terminal interface without external libraries.
- **Dynamic Array Handling**: Allows the user to dynamically input array lengths and elements, manipulating memory pointers (`SI`, `DI`) in real-time.
- **In-Place Sorting**: Implements an O(N²) Bubble Sort algorithm purely in Assembly to enable Median calculations.
- **Standalone CLI**: A massive, interactive ASCII menu driven by keyboard interrupts (`int 16h`).

### How to Run:
1. Open the **EMU8086** IDE.
2. Open the `AsmStat.asm` file.
3. Click the **Emulate** button, then click **Run**.
4. Use the keyboard to navigate the colored menu and perform calculations!

---

## 🧠 Educational Value & Technical Achievements
*   **Cross-Architecture Expertise**: Demonstrates the massive differences between 16-bit segmented real mode and modern 64-bit flat memory models.
*   **Foreign Function Interfaces (FFI)**: Proves the ability to interface high-level scripting languages (Python) with low-level machine code via DLLs and C-types.
*   **Algorithmic Implementation**: Translating complex algorithms (like Bubble Sort and Variance calculation) directly into CPU instructions.
*   **Hardware Interaction**: Using software interrupts to communicate directly with the BIOS/DOS for screen rendering and input capture.

