import streamlit as st
import ctypes
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import platform


# Set wide layout and collapse sidebar
st.set_page_config(page_title="AsmStat Pro", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to massively increase font sizes and make the UI look premium
st.markdown("""
<style>
    /* Global Text Scaling */
    html, body, [class*="css"] {
        font-size: 20px !important;
    }
    
    /* Titles */
    .main-title { font-size: 60px !important; font-weight: 900; color: #FFFFFF; margin-bottom: 0px;}
    .sub-title { font-size: 28px !important; color: #A0AEC0; margin-bottom: 30px;}
    h3 { font-size: 32px !important; font-weight: bold !important; padding-top: 1rem !important; }
    h4 { font-size: 26px !important; font-weight: bold !important; }
    
    /* Inputs & Selectboxes */
    .stTextInput > div > div > input { font-size: 28px !important; padding: 20px !important; font-weight: bold; text-align: center;}
    .stSelectbox label, .stFileUploader label { font-size: 22px !important; font-weight: bold !important; color: #E2E8F0 !important;}
    .stSelectbox div[data-baseweb="select"] { font-size: 22px !important; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button { font-size: 26px !important; font-weight: bold !important; padding: 15px 30px !important; }
    
    /* Dataframes / Tables */
    .stDataFrame { font-size: 20px !important; }
    [data-testid="stDataFrame"] div { font-size: 18px !important; }
    
    /* Metric Cards */
    .metric-box { background-color: #1E1E1E; padding: 30px; border-radius: 15px; text-align: center; border: 1px solid #333; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-top: 20px;}
    .metric-value { font-size: 55px !important; font-weight: 900; color: #4FD1C5; margin: 0; }
    .metric-label { font-size: 24px !important; font-weight: 700; color: #E2E8F0; text-transform: uppercase; letter-spacing: 2px;}
    
    /* General text */
    p { font-size: 22px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<p class='main-title'>🚀 AsmStat Pro Max</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>High-Performance Statistical Engine: 100% 64-bit Assembly Backend</p>", unsafe_allow_html=True)

# --- Load the Assembly DLL ---

@st.cache_resource
def load_asm_library():
    base_dir = os.path.dirname(__file__)
    if platform.system() == "Windows":
        dll_path = os.path.join(base_dir, "math.dll")
    else:
        dll_path = os.path.join(base_dir, "libmath.so")

    if not os.path.exists(dll_path):
        return None
    try:
        lib = ctypes.CDLL(dll_path)

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
    st.error("⚠️ `math.dll` not found. Please run `build.bat` to compile the Assembly code first!")
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
    st.markdown("### 📊 Upload a CSV Dataset")
    uploaded_file = st.file_uploader("Upload CSV (must contain numeric columns)", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
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
            st.error(f"Error reading CSV: {e}")

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
