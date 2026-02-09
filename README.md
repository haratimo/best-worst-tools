# Best-Worst Scaling (aka MaxDiff) Tools

A comprehensive suite of tools for generating and scoring Best-Worst Scaling (BWS) experiments, originally developed by Dr Geoff Hollis (University of Alberta).

> [!IMPORTANT]
> **New to Best-Worst Scaling? Use the Streamlit GUI!**
> If you are a researcher who wants a user-friendly, point-and-click experience without worrying about code or command-line syntax, go directly to the `bestworst_tools_streamlit` folder. It provides a visual web interface to handle everything from trial generation to data scoring.

---

## 📂 Project Structure

```bash
.
├── bestworst_tools_legacy_python2  # Original source code (archival)
│   ├── README.txt                  # Original instructions
│   ├── samples/                    # Sample data
│   └── scripts/                    # Legacy Python 2.7 files
├── bestworst_tools_python3         # Refactored for Python 3 (power users)
│   ├── MIGRATION_SUMMARY.txt       # Technical validation & tests
│   ├── README.txt                  # Updated usage instructions
│   ├── samples/                    # Test data
│   ├── scripts/                    # Refactored Python 3 files
│   └── UPDATES.txt                 # Detailed change log
├── bestworst_tools_streamlit       # User-friendly Web GUI (Recommended)
│   ├── app.py                      # Main application
│   ├── README.md                   # Installation & User Guide
│   ├── requirements.txt            # App dependencies
│   └── run_app.sh                  # One-click launch script
└── README.md                       # This file
```

---

## 📂 Folder Overview

This repository is organized into three main versions of the tools:

### 1. [Streamlit GUI](file:///media/parastoo/0EFE0F0B0EFE0F0B/Experiments_UofA/Experiments/bestworst_tools_Hollis_original/bestworst_tools_streamlit/)
**Location:** `/bestworst_tools_streamlit/`  
**Target User:** Researchers, students, and industry professionals.  
**Why use it?** 
- **Easy UI**: Drag-and-drop file uploads and interactive settings.
- **Smart Detection**: Automatically detects spreadsheet columns for your items.
- **No Coding**: No need to write scripts or use the terminal beyond the initial launch.
- **All-in-One**: Combines trial creation and data scoring in one web app.

### 2. [Python 3 (Refactored)](file:///media/parastoo/0EFE0F0B0EFE0F0B/Experiments_UofA/Experiments/bestworst_tools_Hollis_original/bestworst_tools_python3/)
**Location:** `/bestworst_tools_python3/`  
**Target User:** Data scientists, programmers, and power users.  
**Why use it?** 
- **Automation**: Easily scriptable for large-batch simulations or automated pipelines.
- **Modern**: Fully migrated to Python 3 with refactored code for better performance.
- **Scientific Validation**: Includes the full simulation engine used in Dr Geoff Hollis's original research.

### 3. [Legacy Version (Python 2.7)](file:///media/parastoo/0EFE0F0B0EFE0F0B/Experiments_UofA/Experiments/bestworst_tools_Hollis_original/bestworst_tools_legacy_python2/)
**Location:** `/bestworst_tools_legacy_python2/`  
**Target User:** Researchers maintaining old projects or using isolated Python 2 environments.  
**Note:** This is the original codebase as developed by Dr Geoff Hollis. It remains here for archival and reproducibility purposes.

---

## 🛠️ Quick Start

### Option A: The GUI (Recommended)
1. Install Streamlit: `pip install streamlit`
2. Navigate to `bestworst_tools_streamlit/`
3. Launch: `streamlit run app.py`

### Option B: Command Line (Python 3)
1. Navigate to `bestworst_tools_python3/`
2. Example (Trial Gen): `python3 scripts/create_trials.py samples/anew_words.txt 8000 4 > trials.csv`
3. Example (Scoring): `python3 scripts/score_trials.py samples/aoa_raw_data/*.csv > results.csv`

---

## 📑 Documentation
- **Technical Changes**: See [UPDATES.txt](file:///media/parastoo/0EFE0F0B0EFE0F0B/Experiments_UofA/Experiments/bestworst_tools_Hollis_original/bestworst_tools_python3/UPDATES.txt) for a log of the refactor.
- **Detailed Summary**: See [MIGRATION_SUMMARY.txt](file:///media/parastoo/0EFE0F0B0EFE0F0B/Experiments_UofA/Experiments/bestworst_tools_Hollis_original/bestworst_tools_python3/MIGRATION_SUMMARY.txt) for scientific validation and test results.
- **GUI Guide**: See [README.md](file:///media/parastoo/0EFE0F0B0EFE0F0B/Experiments_UofA/Experiments/bestworst_tools_Hollis_original/bestworst_tools_streamlit/README.md) inside the Streamlit folder.

---

## ⚖️ License & Attribution

**Original Author:** Dr Geoff Hollis  
**Migration & Refactor:** Parastoo Harati (p.harati@ualberta.ca)  
**Finalized:** December 15, 2023  

**Citation:**
Hollis, G. (2017). Scoring best/worst data in unbalanced, many-item designs, with applications to crowdsourcing semantic judgments. *Behavior Research Methods*, 1-19. doi: 10.3758/s13428-017-0898-2

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

---

## 🙏 Acknowledgments

We honor the memory of Dr Geoff Hollis, whose innovative work continues to benefit researchers worldwide. This project aims to make his tools accessible to a broader audience, including those who may not be comfortable with command-line interfaces.
