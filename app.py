import streamlit as st
import ctypes
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import platform
import subprocess
import shutil

st.set_page_config(page_title="AsmStat Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
/* Modern typography */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Outfit', sans-serif !important;
}

/* Background gradient for the whole app */
.stApp {
    background: linear-gradient(135deg, #020617 0%, #1e1b4b 50%, #0f172a 100%);
    color: #f8fafc;
}

/* Hide streamlit header and footer */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Glassmorphism Metric Cards */
.metric-box {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 24px;
    margin: 10px 0px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.4s ease, box-shadow 0.4s ease;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-box::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
    transition: left 0.5s ease;
}
.metric-box:hover::before {
    left: 100%;
}
.metric-box:hover {
    transform: translateY(-8px);
    border-color: rgba(168, 85, 247, 0.5); /* Purple glow */
    box-shadow: 0 15px 40px rgba(168, 85, 247, 0.25);
    background: rgba(255, 255, 255, 0.05);
}
.metric-label {
    font-size: 1.1rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 12px;
    font-weight: 600;
}
.metric-value {
    font-size: 2.8rem;
    color: #f8fafc;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.2;
}

/* Modernize tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background-color: transparent;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255,255,255,0.02);
    border-radius: 12px 12px 0 0;
    border: 1px solid rgba(255,255,255,0.05);
    border-bottom: none;
    padding: 12px 24px;
    transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(255,255,255,0.05);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, rgba(168, 85, 247, 0.15) 0%, transparent 100%) !important;
    border-top: 2px solid #a855f7 !important;
    border-left: 1px solid rgba(168, 85, 247, 0.3) !important;
    border-right: 1px solid rgba(168, 85, 247, 0.3) !important;
}
.stTabs [aria-selected="true"] p {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* Styled text inputs and file uploaders */
.stTextInput input, .stSelectbox > div > div {
    background-color: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(148, 163, 184, 0.2) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 14px !important;
    transition: all 0.3s ease;
    font-family: 'Outfit', sans-serif;
}
.stTextInput input:focus, .stSelectbox > div > div:focus-within {
    border-color: #a855f7 !important;
    box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2) !important;
    background-color: rgba(15, 23, 42, 0.8) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
    background-size: 200% auto;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 2.5rem;
    font-weight: 600;
    transition: 0.5s;
    box-shadow: 0 4px 15px 0 rgba(168, 85, 247, 0.4);
    font-family: 'Outfit', sans-serif;
}
.stButton > button:hover {
    background-position: right center; /* trigger gradient animation */
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(168, 85, 247, 0.6);
    color: white;
}

/* Dataframe glass effect */
[data-testid="stDataFrame"] {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 15px;
    box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
}

/* Headings */
h1, h2, h3 {
    background: linear-gradient(90deg, #f8fafc, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

/* Dividers */
hr {
    border-color: rgba(255,255,255,0.08);
    margin: 3rem 0;
}

/* Streamlit specific hide main padding top */
.css-18e3th9 {
    padding-top: 2rem;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Custom Animated Header
st.markdown("""
<div style='text-align: center; padding: 3rem 0; margin-bottom: 2.5rem; background: rgba(255,255,255,0.02); border-radius: 24px; border: 1px solid rgba(255,255,255,0.05); backdrop-filter: blur(12px); box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
    <h1 style='font-size: 4rem; margin-bottom: 0; background: linear-gradient(90deg, #3b82f6, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; letter-spacing: -1px;'>AsmStat Pro</h1>
    <p style='color: #94a3b8; font-size: 1.2rem; margin-top: 10px; font-weight: 300; letter-spacing: 1px;'>HIGH-PERFORMANCE ASSEMBLY-POWERED DATA SCIENCE ENGINE</p>
</div>
""", unsafe_allow_html=True)

def _build_linux_library(base_dir):
    """Compile math_linux.asm → libmath.so on Linux (Streamlit Cloud)."""
    asm_src = os.path.join(base_dir, "math_linux.asm")
    obj_path = os.path.join(base_dir, "math_linux.o")
    lib_path = os.path.join(base_dir, "libmath.so")

    if not os.path.exists(asm_src):
        st.error("❌ `math_linux.asm` not found — cannot compile on Linux.")
        return None

    # Check that nasm and ld are available
    if not shutil.which("nasm"):
        st.error("❌ `nasm` not installed. Add it to `packages.txt`.")
        return None
    if not shutil.which("ld"):
        st.error("❌ `ld` (linker) not installed. Add `binutils` to `packages.txt`.")
        return None

    try:
        # Assemble
        result = subprocess.run(
            ["nasm", "-f", "elf64", asm_src, "-o", obj_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            st.error(f"❌ NASM assembly failed:\n```\n{result.stderr}\n```")
            return None

        # Link into shared library
        result = subprocess.run(
            ["ld", "-shared", "-z", "noexecstack", "-o", lib_path, obj_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            st.error(f"❌ Linking failed:\n```\n{result.stderr}\n```")
            return None

        return lib_path
    except Exception as e:
        st.error(f"❌ Build error: {e}")
        return None


@st.cache_resource
def load_asm_library():
    base_dir = os.path.dirname(__file__)
    if platform.system() == "Windows":
        lib_path = os.path.join(base_dir, "math.dll")
    else:
        lib_path = os.path.join(base_dir, "libmath.so")

    # On Linux, compile from source if the .so is missing or stale
    if platform.system() != "Windows":
        asm_src = os.path.join(base_dir, "math_linux.asm")
        needs_build = not os.path.exists(lib_path)
        if not needs_build and os.path.exists(asm_src):
            # Rebuild if the .asm source is newer than the compiled .so
            needs_build = os.path.getmtime(asm_src) > os.path.getmtime(lib_path)
        if needs_build:
            # Remove stale .so if it exists
            if os.path.exists(lib_path):
                os.remove(lib_path)
            lib_path = _build_linux_library(base_dir)
            if lib_path is None:
                return None

    if not os.path.exists(lib_path):
        return None

    try:
        lib = ctypes.CDLL(lib_path)

        # Wire up functions
        for func_name in ['asm_sum', 'asm_mean', 'asm_variance', 'asm_min', 'asm_max']:
            func = getattr(lib, func_name)
            func.argtypes = [ctypes.POINTER(ctypes.c_longlong), ctypes.c_longlong]
            func.restype = ctypes.c_longlong

        lib.asm_stddev.argtypes = [ctypes.POINTER(ctypes.c_longlong), ctypes.c_longlong]
        lib.asm_stddev.restype = ctypes.c_double

        lib.asm_dot_product.argtypes = [
            ctypes.POINTER(ctypes.c_longlong),
            ctypes.POINTER(ctypes.c_longlong),
            ctypes.c_longlong
        ]
        lib.asm_dot_product.restype = ctypes.c_longlong

        return lib
    except Exception as e:
        st.error(f"Error loading library: {e}")
        return None

asm_lib = load_asm_library()

if asm_lib is None:
    st.error("⚠️ Assembly library not found. On Windows: run build.bat → math.dll. On Linux: ensure nasm + binutils are in packages.txt.")
    st.stop()


DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CLI_SYNC_FILE = r"D:\ASMSTAT.TXT"


def get_cli_search_paths():
    """Locations where the EMU8086 CLI may write synced data."""
    return [
        CLI_SYNC_FILE,
        os.path.join(DATA_DIR, "DATA.TXT"),
        os.path.join(DATA_DIR, "data.txt"),
        r"D:\DATA.TXT",
        r"C:\emu8086\vdrive\C\DATA.TXT",
        r"C:\emu8086\MyBuild\DATA.TXT",
        r"C:\emu8086\DATA.TXT"
    ]


def parse_cli_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        return None
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    return values if values else None


def load_cli_data():
    """Read array saved by the EMU8086 CLI (Option 1)."""
    for path in get_cli_search_paths():
        if not os.path.exists(path):
            continue
        try:
            values = parse_cli_file(path)
            if values:
                return values, path
        except (ValueError, OSError):
            continue
    return None, None


def get_cli_path_status():
    """Help debug sync issues by showing which paths exist."""
    status = []
    for path in get_cli_search_paths():
        if os.path.exists(path):
            try:
                size = os.path.getsize(path)
                status.append(f"`{path}` — found ({size} bytes)")
            except OSError:
                status.append(f"`{path}` — found (unreadable)")
        else:
            status.append(f"`{path}` — not found")
    return status


cli_data, cli_file = load_cli_data()
cli_default = ", ".join(str(x) for x in cli_data) if cli_data else "10, 20, 30, 40, 50, 60, 70, 80, 90"

tab_cli, tab1, tab2 = st.tabs(["🖥️ CLI Sync", "📝 Manual Input", "📂 CSV Upload"])

manual_arr = None
csv_arr = None
uploaded_file = None
df = None

with tab_cli:
    st.markdown("### 🔗 Auto-Sync from EMU8086 CLI")
    st.caption(
        "After entering data with **Option 1** in EMU8086, click **Compile** (or press F5) to rebuild, "
        f"then run again. Data is saved to `{CLI_SYNC_FILE}`."
    )
    if cli_data:
        modified = os.path.getmtime(cli_file)
        modified_str = pd.Timestamp(modified, unit="s").strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"**{len(cli_data)} elements** loaded from `{cli_file}` (updated {modified_str})")
        st.code(", ".join(str(x) for x in cli_data), language=None)
    else:
        st.warning(
            "No CLI data found yet. In EMU8086: open `AsmStat.asm` → **Compile** → **Run** → "
            "**Option 1** → enter elements → then click **Refresh from CLI** below."
        )
        with st.expander("Where is the app looking for data?"):
            for line in get_cli_path_status():
                st.markdown(f"- {line}")
    if st.button("🔄 Refresh from CLI"):
        st.rerun()

with tab1:
    st.markdown("### 🔢 Enter Your Dataset (Comma Separated)")
    user_input = st.text_input("", cli_default, key="manual_input")
    try:
        data_list = [int(x.strip()) for x in user_input.split(',') if x.strip()]
        if data_list:
            manual_arr = np.array(data_list, dtype=np.int64)
    except ValueError:
        st.error("Invalid input! Please enter only valid integers separated by commas.")

with tab2:
    st.markdown("### 📊 Upload a Dataset (CSV/Excel)")
    uploaded_file = st.file_uploader("Upload Dataset (must contain numeric columns)", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        try:
            filename = uploaded_file.name.lower()
            if filename.endswith(".csv"):
                # Try multiple encodings for robustness
                encodings_to_try = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
                df = None
                for enc in encodings_to_try:
                    try:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, encoding=enc)
                        break
                    except Exception:
                        continue
                if df is None:
                    st.error("Failed to decode the CSV file with standard encodings (utf-8, latin1, cp1252).")
            else:
                df = pd.read_excel(uploaded_file)
            
            if df is not None:
                st.write("Preview of Dataset:", df.head())
                numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
                if not numeric_cols:
                    st.error("No numeric columns found in the dataset.")
                else:
                    selected_col = st.selectbox("Select a column to analyze:", numeric_cols)
                    # Drop NaNs and convert to int64 for Assembly
                    csv_arr = df[selected_col].dropna().astype(np.int64).values
                    
                    # Check for second column for dot product
                    if len(numeric_cols) > 1:
                        st.markdown("#### ✖️ Dot Product")
                        col2_sel = st.selectbox("Select a second column for Dot Product (must be same length):", ["None"] + numeric_cols)
                        if col2_sel != "None":
                            arr2 = df[col2_sel].dropna().astype(np.int64).values
                            if len(arr2) == len(csv_arr):
                                c_arr1 = csv_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong))
                                c_arr2 = arr2.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong))
                                dp_val = asm_lib.asm_dot_product(c_arr1, c_arr2, len(csv_arr))
                                st.success(f"**Dot Product Result:** {dp_val}")
                            else:
                                st.warning("Columns must be of the same length to calculate dot product.")
        except Exception as e:
            st.error(f"Error reading dataset: {e}")

arr = None
length = 0
data_source = None

if csv_arr is not None and len(csv_arr) > 0:
    arr = csv_arr
    length = len(arr)
    data_source = "CSV Upload"
elif cli_data:
    arr = np.array(cli_data, dtype=np.int64)
    length = len(arr)
    data_source = f"CLI Sync ({os.path.basename(cli_file)})"
elif manual_arr is not None and len(manual_arr) > 0:
    arr = manual_arr
    length = len(manual_arr)
    data_source = "Manual Input"

if data_source:
    st.markdown(f"<p style='font-size:18px;color:#A0AEC0;'>Active dataset: <b>{data_source}</b></p>", unsafe_allow_html=True)

if arr is not None and length > 0:
    c_arr = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong))
    
    # --- Execute Assembly Functions ---
    with st.spinner("Executing 64-bit Assembly..."):
        asm_sum_val = asm_lib.asm_sum(c_arr, length)
        asm_mean_val = asm_lib.asm_mean(c_arr, length)
        asm_var_val = asm_lib.asm_variance(c_arr, length)
        asm_stddev_val = asm_lib.asm_stddev(c_arr, length)
        asm_min_val = asm_lib.asm_min(c_arr, length)
        asm_max_val = asm_lib.asm_max(c_arr, length)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Massive Custom Metrics UI ---
    st.markdown("### ⚡ Assembly Calculation Results")
    col1, col2, col3, col4 = st.columns(4)
    
    def metric_card(label, value, col):
        col.markdown(f"""
        <div class="metric-box">
            <p class="metric-label">{label}</p>
            <p class="metric-value">{value}</p>
        </div>
        """, unsafe_allow_html=True)

    metric_card("Sum", asm_sum_val, col1)
    metric_card("Mean", asm_mean_val, col2)
    metric_card("Variance", asm_var_val, col3)
    metric_card("Std Dev", f"{asm_stddev_val:.2f}", col4)

    col5, col6, col7, _ = st.columns(4)
    metric_card("Min", asm_min_val, col5)
    metric_card("Max", asm_max_val, col6)
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    # --- Advanced Plotly Visualizations ---
    st.markdown("### 📊 Interactive Data Analytics")
    
    # Row 1 of Graphs
    g_col1, g_col2 = st.columns(2)
    
    # 1. Bar Chart with Min/Max/Mean indicators
    with g_col1:
        fig1 = go.Figure()
        # Limit to 100 points for bar chart if dataset is huge
        plot_arr = arr[:100]
        colors = ['#3182ce' if x not in [asm_min_val, asm_max_val] else ('#e53e3e' if x == asm_min_val else '#38a169') for x in plot_arr]
        fig1.add_trace(go.Bar(y=plot_arr, x=list(range(len(plot_arr))), marker_color=colors, text=plot_arr, textposition='auto'))
        fig1.add_hline(y=asm_mean_val, line_dash="dash", line_color="orange", annotation_text=f"Mean: {asm_mean_val}")
        fig1.update_layout(title="Array Distribution (First 100, Red=Min, Green=Max)", xaxis_title="Index", yaxis_title="Value", template="plotly_dark", height=400)
        st.plotly_chart(fig1, use_container_width=True)

    # 2. Line Trend Chart
    with g_col2:
        fig2 = px.line(x=list(range(len(plot_arr))), y=plot_arr, markers=True, title="Data Trend Analysis (First 100)")
        fig2.update_traces(line_color='#9f7aea', marker=dict(size=10, color='white'))
        fig2.update_layout(xaxis_title="Index", yaxis_title="Value", template="plotly_dark", height=400)
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2 of Graphs
    g_col3, g_col4 = st.columns(2)
    
    # 3. Box Plot (Great for showing Variance/Spread)
    with g_col3:
        fig3 = px.box(y=arr, title="Statistical Spread (Box Plot)", points="all")
        fig3.update_traces(marker_color='#ed8936')
        fig3.update_layout(yaxis_title="Value", template="plotly_dark", height=400)
        st.plotly_chart(fig3, use_container_width=True)
        
    # 4. Histogram
    with g_col4:
        fig4 = px.histogram(x=arr, nbins=min(20, length), title="Frequency Histogram")
        fig4.update_traces(marker_color='#48bb78', marker_line_color='black', marker_line_width=1)
        fig4.update_layout(xaxis_title="Value", yaxis_title="Count", template="plotly_dark", height=400)
        st.plotly_chart(fig4, use_container_width=True)

    # Row 3: Z-Scores
    st.markdown("### 📈 Z-Score Analysis")
    st.write("Calculated efficiently in Python using the `Mean` and `Standard Deviation` rapidly computed by the Assembly backend.")
    if asm_stddev_val > 0:
        z_scores = (arr - asm_mean_val) / asm_stddev_val
        fig4 = px.histogram(x=z_scores, nbins=min(20, length), title="Z-Score Distribution")
        fig4.update_traces(marker_color='#9f7aea', marker_line_color='black', marker_line_width=1)
        fig4.update_layout(xaxis_title="Z-Score", yaxis_title="Count", template="plotly_dark", height=400)
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Standard Deviation is 0, so Z-Scores are undefined.")

    # Row 4: Advanced Distributions
    st.markdown("### 🔬 Advanced Distribution Analysis")
    g_col5, g_col6 = st.columns(2)
    with g_col5:
        # Violin Plot
        fig5 = px.violin(y=arr, box=True, points="all", title="Violin Plot (Density & Spread)")
        fig5.update_traces(marker_color='#38b2ac')
        fig5.update_layout(yaxis_title="Value", template="plotly_dark", height=400)
        st.plotly_chart(fig5, use_container_width=True)
        
    with g_col6:
        # ECDF Plot (Empirical Cumulative Distribution Function)
        fig6 = px.ecdf(x=arr, title="Empirical Cumulative Distribution (ECDF)")
        fig6.update_traces(line_color='#e53e3e', line_width=3)
        fig6.update_layout(xaxis_title="Value", yaxis_title="Probability", template="plotly_dark", height=400)
        st.plotly_chart(fig6, use_container_width=True)

    # Row 5: Advanced Outlier Detection (IQR)
    st.markdown("### 🚨 Outlier Detection (IQR Method)")
    Q1 = np.percentile(arr, 25)
    Q3 = np.percentile(arr, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = arr[(arr < lower_bound) | (arr > upper_bound)]
    
    col_out1, col_out2 = st.columns([1, 2])
    with col_out1:
        st.info(f"**Q1 (25%)**: {Q1:.2f}\n\n**Q3 (75%)**: {Q3:.2f}\n\n**IQR**: {IQR:.2f}")
        if len(outliers) > 0:
            st.warning(f"Found **{len(outliers)}** outliers out of {length} points.")
        else:
            st.success("No significant outliers detected.")
    with col_out2:
        if len(outliers) > 0:
            outlier_indices = np.where((arr < lower_bound) | (arr > upper_bound))[0]
            fig_out = px.scatter(x=outlier_indices, y=outliers, title="Detected Outliers", color_discrete_sequence=['red'])
            fig_out.update_traces(marker=dict(size=10, symbol='x'))
            fig_out.update_layout(xaxis_title="Original Array Index", yaxis_title="Outlier Value", template="plotly_dark", height=300)
            st.plotly_chart(fig_out, use_container_width=True)
        else:
            st.success("The dataset contains no extreme values based on the 1.5 * IQR rule. ✨")

    # Row 6: Time-Series / Rolling Analysis (if dataset is large enough)
    if length > 5:
        st.markdown("### 🎢 Sequential & Rolling Analysis")
        ts_col1, ts_col2 = st.columns(2)
        with ts_col1:
            # Cumulative Sum
            cumsum_arr = np.cumsum(arr)
            fig_ts1 = px.line(x=list(range(length)), y=cumsum_arr, title="Cumulative Sum Over Index")
            fig_ts1.update_traces(line_color='#d69e2e')
            fig_ts1.update_layout(xaxis_title="Index", yaxis_title="Cumulative Sum", template="plotly_dark", height=400)
            st.plotly_chart(fig_ts1, use_container_width=True)
        with ts_col2:
            # Simple Moving Average (window=min(5, length//5))
            window = max(2, min(10, length // 5))
            sma = pd.Series(arr).rolling(window=window).mean().values
            fig_ts2 = px.line(x=list(range(length)), y=arr, title=f"Value Trend with {window}-Point Moving Average")
            fig_ts2.update_traces(opacity=0.5)
            fig_ts2.add_scatter(x=list(range(length)), y=sma, mode='lines', name=f'{window}-pt SMA', line=dict(color='yellow', width=3))
            fig_ts2.update_layout(xaxis_title="Index", yaxis_title="Value", template="plotly_dark", height=400, showlegend=False)
            st.plotly_chart(fig_ts2, use_container_width=True)

if df is not None:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("## 🌐 Full Dataset Exploratory Data Analysis (EDA)")
    
    # Show dataset shape and head
    st.markdown(f"**Dataset Shape:** `{df.shape[0]} Rows` × `{df.shape[1]} Columns`")
    with st.expander("View Raw Dataset Statistics", expanded=False):
        st.dataframe(df.describe(), use_container_width=True)
    
    st.markdown("### 🧩 Missing Values Analysis")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        fig_missing = px.bar(x=missing.index, y=missing.values, title="Missing Values per Column", labels={'x': 'Column', 'y': 'Missing Count'})
        fig_missing.update_traces(marker_color='#d69e2e')
        fig_missing.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_missing, use_container_width=True)
    else:
        st.success("No missing values found in the uploaded dataset! ✨")

    st.markdown("### 🎯 Individual Column Deep-Dive Analysis")
    numeric_df = df.select_dtypes(include=np.number)
    numeric_columns = numeric_df.columns.tolist()
    if numeric_columns:
        deep_col = st.selectbox("Select a column to analyze its detailed statistics:", numeric_columns, key="eda_col_select")
        col_data = df[deep_col].dropna()
        
        # Calculate stats
        col_sum = col_data.sum()
        col_mean = col_data.mean()
        col_var = col_data.var()
        col_std = col_data.std()
        col_min = col_data.min()
        col_max = col_data.max()
        
        def safe_fmt(val):
            return f"{val:,.2f}" if isinstance(val, (int, float)) else str(val)

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="metric-box"><p class="metric-label">SUM</p><p class="metric-value" style="font-size:2rem;">{safe_fmt(col_sum)}</p></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-box"><p class="metric-label">MEAN</p><p class="metric-value" style="font-size:2rem;">{safe_fmt(col_mean)}</p></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-box"><p class="metric-label">VARIANCE</p><p class="metric-value" style="font-size:2rem;">{safe_fmt(col_var)}</p></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-box"><p class="metric-label">STD DEV</p><p class="metric-value" style="font-size:2rem;">{safe_fmt(col_std)}</p></div>', unsafe_allow_html=True)
        
        c5, c6, c7, c8 = st.columns(4)
        c5.markdown(f'<div class="metric-box"><p class="metric-label">MIN</p><p class="metric-value" style="font-size:2rem;">{safe_fmt(col_min)}</p></div>', unsafe_allow_html=True)
        c6.markdown(f'<div class="metric-box"><p class="metric-label">MAX</p><p class="metric-value" style="font-size:2rem;">{safe_fmt(col_max)}</p></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 🧮 Numeric Feature Correlation")
    numeric_df = df.select_dtypes(include=np.number)
    if len(numeric_df.columns) > 1:
        corr = numeric_df.corr()
        fig_corr = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Heatmap", color_continuous_scale="RdBu_r")
        fig_corr.update_layout(template="plotly_dark", height=500)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.markdown("### 📈 Scatter Matrix (Pairplot)")
        # Limit columns to max 5 for performance
        cols_to_plot = numeric_df.columns[:min(5, len(numeric_df.columns))]
        fig_splom = px.scatter_matrix(numeric_df, dimensions=cols_to_plot, title=f"Scatter Matrix (First {len(cols_to_plot)} Numeric Columns)")
        fig_splom.update_layout(template="plotly_dark", height=800)
        st.plotly_chart(fig_splom, use_container_width=True)
    else:
        st.info("Not enough numeric columns for multivariate correlation or pairplots.")
