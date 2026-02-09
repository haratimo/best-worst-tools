"""
Best-Worst Scaling (aka MaxDiff) Tools - Streamlit Web Interface

A user-friendly graphical interface for the best-worst scaling (aka MaxDiff) tools
originally created by Geoff Hollis.

Original Author: Geoff Hollis
Python 3 migration, refactor, and GUI build: Parastoo Harati (p.harati@ualberta.ca)
Streamlit GUI: Parastoo Harati (p.harati@ualberta.ca)
Date: December 15, 2023
"""

import streamlit as st
import sys
import os
import io
import tempfile
from pathlib import Path

# Add parent directory to path to import from bestworst_tools_python3
parent_dir = Path(__file__).parent.parent / "bestworst_tools_python3" / "scripts"
sys.path.insert(0, str(parent_dir))

import trialgen
import scoring
from spreadsheet import Spreadsheet

# Page configuration
st.set_page_config(
    page_title="Best-Worst Scaling (aka MaxDiff) Tools",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📊 Best-Worst-Tools ")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "Choose a tool:",
    ["🏠 Home", "🎲 Create Trials", "📈 Score Data", "ℹ️ About"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Original Author:**  
Geoff Hollis

**Python 3 migration, refactor, and GUI build:**  
Parastoo Harati  
p.harati@ualberta.ca

**Citation:**  
Hollis, G. (2017). Behavior Research Methods.  
doi: 10.3758/s13428-017-0898-2
""")


def home_page():
    """Display the home page"""
    st.markdown('<p class="main-header">Best-Worst Scaling (aka MaxDiff) Tools</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">A graphical interface for creating and scoring best-worst trials</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎲 Create Trials")
        st.markdown("""
        Generate best-worst trials from a list of items (words, images, etc.).
        
        **You'll need:**
        - A text file (.txt) OR a spreadsheet (.csv/.tsv)
        - In the spreadsheet format, the program handles multiple columns and lets you choose your item column.
        
        **You'll get:**
        - Optimally generated trials ready for your experiment
        - CSV file with trial combinations
        """)
        
    with col2:
        st.markdown("### 📈 Score Data")
        st.markdown("""
        Analyze collected best-worst data and generate item scores.
        
        **You'll need:**
        - CSV files with participant responses
        - Columns: best, worst, option1, option2, ...
        
        **You'll get:**
        - Latent scores for each item
        - Multiple scoring methods (Value, Elo, etc.)
        """)
    
    st.markdown("---")
    
    st.info("👈 **Get started by selecting a tool from the sidebar**")
    
    with st.expander("📖 Quick Guide"):
        st.markdown("""
        ### How to use this tool:
        
        1. **Creating Trials**
           - Upload a list of items (words, stimuli, etc.)
           - Set parameters (number of trials, items per trial)
           - Download the generated trials CSV
        
        2. **Scoring Data**
           - Upload participant response files
           - Select scoring method(s)
           - Download the scored results
        
        3. **Running Your Experiment**
           - Use the generated trials in your experiment platform
           - Collect "best" and "worst" choices from participants
           - Upload the data back here to get scores
        """)


def create_trials_page():
    """Create trials interface"""
    st.markdown('<p class="main-header">🎲 Create Best-Worst Trials</p>', unsafe_allow_html=True)
    st.markdown("Generate optimally balanced trials from your list of items")
    
    st.markdown("---")
    
    # Instructions
    with st.expander("ℹ️ How it works", expanded=False):
        st.markdown("""
        This tool creates best-worst trials from a list of items. Each trial presents K items,
        and participants select the "best" and "worst" according to some criterion.
        
        **Input format:**
        - **Plain text file (.txt)**: One item per line
        - **CSV/TSV spreadsheet**: Upload any data file, then select which column contains your items. The refactored engine will extract unique items automatically.
        
        **Parameters:**
        - **N (trials)**: Total number of trials to generate (default: items × 8)
        - **K (items per trial)**: Number of items shown in each trial (default: 4)
        - **Generator**: Algorithm for creating trials (default: norepeateven)
        """)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your items file (.txt, .csv, or .tsv)",
        type=['txt', 'csv', 'tsv'],
        help="Upload a file with your items. For .txt files, one item per line. For CSV/TSV, specify the column below."
    )
    
    if uploaded_file:
        # Determine file type
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if file_extension == 'txt':
                # Read text file
                content = uploaded_file.getvalue().decode('utf-8')
                items = [item.strip() for item in content.split() if item.strip()]
                st.success(f"✅ Loaded {len(items)} items from text file")
                
                with st.expander("Preview items"):
                    st.write(items[:20])
                    if len(items) > 20:
                        st.write(f"... and {len(items) - 20} more items")
            
            else:  # CSV or TSV
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                try:
                    sep = '\t' if file_extension == 'tsv' else ','
                    ss = Spreadsheet.read_csv(tmp_path, delimiter=sep)
                    
                    # Let user select column
                    column_name = st.selectbox("Select the column containing your items:", ss.header)
                    items = [item for item in ss[column_name] if item and len(str(item).strip()) > 0]
                    
                    st.success(f"✅ Loaded {len(items)} items from column '{column_name}'")
                    
                    with st.expander("Preview items"):
                        st.write(items[:20])
                        if len(items) > 20:
                            st.write(f"... and {len(items) - 20} more items")
                finally:
                    os.unlink(tmp_path)
        
        with col2:
            st.metric("Total Items", len(items))
        
        # Parameters
        st.markdown("---")
        st.markdown("### ⚙️ Trial Parameters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            default_n = len(items) * 8
            N = st.number_input(
                "Number of trials (N)",
                min_value=1,
                value=default_n,
                help="Total number of trials to generate. Default is items × 8."
            )
        
        with col2:
            K = st.number_input(
                "Items per trial (K)",
                min_value=2,
                max_value=10,
                value=4,
                help="How many items to show in each trial"
            )
        
        with col3:
            generator = st.selectbox(
                "Generation method",
                ["norepeateven", "even", "random", "norepeat"],
                help="norepeateven = recommended (even distribution, no repeated pairs)"
            )
        
        # Validation
        if (N * K) % len(items) != 0 and generator in ["norepeateven", "even"]:
            st.warning(f"⚠️ For even distribution: N × K must be divisible by {len(items)}. "
                      f"Current: {N} × {K} = {N*K} (not divisible by {len(items)})")
            st.info(f"💡 Suggested N values: {[len(items) * i for i in [4, 6, 8, 10, 12, 16]]}")
        
        # Generate button
        if st.button("🎲 Generate Trials", type="primary", use_container_width=True):
            try:
                with st.spinner("Generating trials..."):
                    # Generate trials
                    if generator == "norepeateven":
                        trials = trialgen.build_trials_even_bigram_norepeat(items, N=N, K=K)
                    elif generator == 'even':
                        trials = trialgen.build_trials_even(items, N=N, K=K)
                    elif generator == 'random':
                        trials = trialgen.build_trials_random(items, N=N, K=K)
                    elif generator == "norepeat":
                        trials = trialgen.build_trials_random_bigram_norepeat(items, N=N, K=K)
                    
                    # Convert to CSV
                    output = io.StringIO()
                    header = [f"option{i+1}" for i in range(K)]
                    output.write(",".join(header) + "\n")
                    for trial in trials:
                        output.write(",".join(trial) + "\n")
                    
                    csv_data = output.getvalue()
                    
                    st.markdown('<div class="success-box">✅ <strong>Trials generated successfully!</strong></div>', 
                               unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Trials Generated", len(trials))
                    with col2:
                        st.metric("Items per Trial", K)
                    with col3:
                        st.metric("Total Presentations", len(trials) * K)
                    
                    # Preview
                    with st.expander("Preview first 10 trials"):
                        preview_lines = csv_data.split('\n')[:11]
                        st.code('\n'.join(preview_lines))
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Trials CSV",
                        data=csv_data,
                        file_name=f"bestworst_trials_N{N}_K{K}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
            except Exception as e:
                st.error(f"❌ Error generating trials: {str(e)}")


def score_data_page():
    """Score data interface"""
    st.markdown('<p class="main-header">📈 Score Best-Worst Data</p>', unsafe_allow_html=True)
    st.markdown("Analyze participant responses and generate item scores")
    
    st.markdown("---")
    
    # Instructions
    with st.expander("ℹ️ How it works", expanded=False):
        st.markdown("""
        Upload CSV files containing participant responses. Each file should have:
        
        **Required columns:**
        - `best`: The item selected as "best"
        - `worst`: The item selected as "worst"
        - `option1`, `option2`, `option3`, ... : All items shown in the trial
        
        **Optional columns:**
        - Participant ID, timestamps, etc. (will be ignored)
        
        **Scoring methods available:**
        - **Value**: Tournament-based, robust to noise (recommended)
        - **Elo**: Chess-style rating system
        - **RW**: Rescorla-Wagner learning model
        - **Best/Worst/Unchosen**: Simple count-based methods
        - And more...
        """)
    
    # File upload
    uploaded_files = st.file_uploader(
        "Upload participant data files (.csv or .tsv)",
        type=['csv', 'tsv'],
        accept_multiple_files=True,
        help="Upload one or more files with participant responses"
    )
    
    if uploaded_files:
        st.success(f"✅ Uploaded {len(uploaded_files)} file(s)")
        
        # Column name configuration
        st.markdown("### ⚙️ Column Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            best_col = st.text_input("Column name for 'best' choice", value="best")
        with col2:
            worst_col = st.text_input("Column name for 'worst' choice", value="worst")
        
        # Scoring methods selection
        st.markdown("### 📊 Select Scoring Methods")
        
        all_methods = ["Value", "Elo", "RW", "Best", "Worst", "Unchosen", 
                      "BestWorst", "ABW", "David", "ValueLogit", "RWLogit", "BestWorstLogit"]
        
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_methods = st.multiselect(
                "Scoring methods to compute:",
                all_methods,
                default=["Value", "Best", "Worst", "BestWorst"],
                help="Select one or more scoring methods. Value is recommended."
            )
        
        with col2:
            if st.button("Select All"):
                selected_methods = all_methods
        
        if not selected_methods:
            st.warning("⚠️ Please select at least one scoring method")
        
        # Score button
        if selected_methods and st.button("📊 Calculate Scores", type="primary", use_container_width=True):
            try:
                with st.spinner("Processing data and calculating scores..."):
                    # Save files temporarily and parse
                    trials = []
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                        
                        try:
                            file_trials = scoring.parse_bestworst_data(
                                tmp_path,
                                bestCol=best_col,
                                worstCol=worst_col
                            )
                            trials.extend(file_trials)
                        finally:
                            os.unlink(tmp_path)
                    
                    if not trials:
                        st.error("❌ No valid trials found in uploaded files")
                        return
                    
                    # Calculate scores
                    results = scoring.score_trials(trials, selected_methods)
                    
                    # Convert to CSV
                    output = io.StringIO()
                    header = ["Item"] + selected_methods
                    output.write(",".join(header) + "\n")
                    
                    for name, data in results.items():
                        if type(name) != str:  # Skip dummy items
                            continue
                        scores = [scoring.scoring_methods[method](data) for method in selected_methods]
                        row = [name] + [str(score) for score in scores]
                        output.write(",".join(row) + "\n")
                    
                    csv_data = output.getvalue()
                    
                    st.markdown('<div class="success-box">✅ <strong>Scoring completed successfully!</strong></div>', 
                               unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Trials Processed", len(trials))
                    with col2:
                        st.metric("Items Scored", len([k for k in results.keys() if type(k) == str]))
                    with col3:
                        st.metric("Methods Used", len(selected_methods))
                    
                    # Preview
                    with st.expander("Preview scores (first 20 items)"):
                        preview_lines = csv_data.split('\n')[:21]
                        st.code('\n'.join(preview_lines))
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Scores CSV",
                        data=csv_data,
                        file_name="bestworst_scores.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
            except Exception as e:
                st.error(f"❌ Error scoring data: {str(e)}")
                st.exception(e)


def about_page():
    """Display about information"""
    st.markdown('<p class="main-header">ℹ️ About Best-Worst Scaling (aka MaxDiff) Tools</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Overview
    
    Best-worst scaling is a research methodology for measuring preferences, perceptions, or any 
    subjective dimension across a set of items. Participants are shown K items at a time and 
    select the "best" and "worst" according to the dimension of interest.
    
    ## Original Work
    
    These tools were originally created by **Geoff Hollis** at the University of Alberta.
    Geoff's pioneering work on best-worst scaling methodologies has been invaluable to the 
    research community.
    
    **Citation:**
    > Hollis, G. (2017). Scoring best/worst data in unbalanced, many-item designs, with 
    > applications to crowdsourcing semantic judgments. *Behavior Research Methods*, XX(X), 1-19. 
    > doi: 10.3758/s13428-017-0898-2
    
    ## Python 3 Migration & GUI
    
    - **Python 3 Update**: Parastoo Harati (p.harati@ualberta.ca)
    - **Streamlit GUI**: Parastoo Harati (p.harati@ualberta.ca)
    - **Date**: December 2023
    
    ## License
    
    This software is released under the Creative Commons license:
    **Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**
    
    https://creativecommons.org/licenses/by-nc-sa/4.0/
    
    ## Scientific Validation & Simulation
    
    The algorithms used in this interface have been rigorously validated through **simulated experiments**. 
    The original tools include a simulation engine (`simulate_results.py`) that uses "virtual participants" 
    to test the accuracy of scoring methods against known truth. 
    
    Simulation allows researchers to:
    - **Prove accuracy**: Compare calculated scores against "true" latent values.
    - **Test noise levels**: See how algorithms perform when data is inconsistent or "noisy."
    - **Optimize designs**: Determine the best N (trials) and K (items) for a specific study.
    
    Geoff Hollis's 2017 research proved that his **Value** method (included here) is exceptionally robust to 
    noise compared to traditional methods like Elo.
    
    ## Acknowledgments
    
    We honor the memory of Geoff Hollis, whose innovative work continues to benefit researchers 
    worldwide. This graphical interface aims to make his tools accessible to a broader audience,
    including those who may not be comfortable with command-line interfaces.
    
    Rest in peace, Geoff.
    """)
    
    st.markdown("---")
    
    with st.expander("📚 Additional Resources"):
        st.markdown("""
        ### Learn More
        
        - **Command-line version**: See the `bestworst_tools_python3/` directory for scripts
        - **Documentation**: Read `README.txt` and `UPDATES.txt` in the Python 3 version
        - **Examples**: Sample data files are in `bestworst_tools_python3/samples/`
        
        ### Support
        
        For questions about:
        - **This GUI or Python 3 version**: Contact Parastoo Harati (p.harati@ualberta.ca)
        - **Original methodology**: See the published paper on the right sidebar
        """)


# Main app routing
if app_mode == "🏠 Home":
    home_page()
elif app_mode == "🎲 Create Trials":
    create_trials_page()
elif app_mode == "📈 Score Data":
    score_data_page()
elif app_mode == "ℹ️ About":
    about_page()
